import argparse
import json
import requests
import sys
import data_loader
import module_loader
import os
import subprocess
import time

def reset_db(script_path):
    args = ["bash", script_path]
    return subprocess.run(args)

def run_okapi(okapi_path, okapi_port, okapi_log):
    args = [ "java", "-jar", "-Dport=%s" % okapi_port, "-Dport_start=%s" % (int(okapi_port) + 1),\
            "-Dport_end=%s" % (int(okapi_port) + 30), okapi_path, "dev"  ]
    proc = None
    if okapi_log:
        out_file = open(okapi_log, 'a')
        proc = subprocess.Popen(args, stdout=out_file, stderr=out_file)
    else:
        proc = subprocess.Popen(args)
    time.sleep(8) #give Okapi a few seconds to spin up
    return proc

def load_module(module_dict, okapi_url, tenant, modules_root, db_conf, node, okapi_proc):
    module_exec = module_dict["exec"].replace('[[MODULES_ROOT]]', modules_root).replace('[[DB_CONF]]', db_conf)
    module_md = module_dict["md"].replace('[[MODULES_ROOT]]', modules_root)
    print("DEBUG: module_exec: %s, module_md: %s" % (module_exec, module_md))
    with open(module_md, 'r') as md_file:
        md_dict = json.load(md_file)
    module_id = md_dict["id"]
    dd_dict = module_loader.make_deployment_descriptor(module_id, module_exec, None, node)
    try:
        module_loader.create_and_deploy_module(okapi_url=okapi_url, module_descriptor=md_dict, deployment_descriptor=dd_dict,\
                tenant=tenant, admin_tenant=None, admin_token=None)
    except Exception as e:
        print("Error loading module %s: %s" % (module_id, e))
        print("Killing Okapi")
        okapi_proc.terminate()
        sys.exit(1)
        #exit

def load_data(endpoint, path, okapi_url, tenant):
    data_loader.load_directory(os.path.abspath(path), okapi_url, endpoint, None, tenant)



def create_tenant(okapi_url, tenant, tenant_name, tenant_desc):
    headers = {
            "Content-Type" : "application/json"
    }
    tenant_dict = {
            "id" : tenant,
            "name" : tenant_name,
            "description" : tenant_desc
    }
    response = requests.post("%s/_/proxy/tenants" % okapi_url, headers=headers, json=tenant_dict)
    return response

if __name__ == "__main__":
    config = {}
    modules = {}
    data_load = {}
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-reload", help="Do not reload Postgres", action="store_true")
    parser.add_argument("--exclude-modules", help="A list of modules to exclude")
    parser.add_argument("--include-modules", help="A list of modules to include")
    parser.add_argument("--module-conf", help="A JSON formatted file defining our modules")
    parser.add_argument("--runtime-conf", help="A JSON formatted file with essential runtime definitions")
    parser.add_argument("--load-data-conf", help="A JSON formatted file with definitions on data to load")
    parser.add_argument("--regular-module-load-list", help="A comma separated list of modules to load, in order")
    parser.add_argument("--auth-module-load-list", help="A comma separated list of auth filter modules to load, in order")
    parser.add_argument("--okapi-path", help="The Okapi jar")
    parser.add_argument("--modules-root", help="The root directory for locating modules")
    parser.add_argument("--db-conf", help="The configuration file for the database")
    parser.add_argument("--okapi-host", help="The host Okapi will run on")
    parser.add_argument("--okapi-port", help="The port for Okapi to run on")
    parser.add_argument("--db-reset-script", help="Bash script to reset db")

    args = parser.parse_args()
    
    if args.runtime_conf:
        with open(os.path.abspath(args.runtime_conf), 'r') as runtime_conf_handle:
            config = json.load(runtime_conf_handle)

    if args.module_conf:
        with open(os.path.abspath(args.module_conf), 'r') as module_conf_handle:
            module_config = json.load(module_conf_handle)
            config["modules"] = module_config

    if args.load_data_conf:
        with open(os.path.abspath(args.load_data_conf), 'r') as load_data_conf_handle:
            data_load_list = json.load(load_data_conf_handle)["data"]
            config["data_load_list"] = data_load_list

    if args.regular_module_load_list:
        config["module_load_list"] = args.regular_module_load_list.split(",")

    if args.auth_module_load_list:
        config["auth_module_load_list"] = args.auth_module_load_list.split(",")

    for arg in [ "okapi_path", "modules_root", "okapi_host", "okapi_port", "db_conf" ]:
        if getattr(args, arg, None):
            config[arg] = getattr(args, arg)

    if not config.get("okapi_host", None):
        config["okapi_host"] = "localhost"

    if not config.get("okapi_port", None):
        config["okapi_port"] = 9130

    print("Current configuration: %s" % json.dumps(config))
    
    if not args.no_reload:
        print("Resetting db")
        completed = reset_db(config["db_reset_script"])
        if(completed.returncode != 0):
            print("Error resetting db, got code %s" % completed.returncode)
            sys.exit(1)


    print("Starting Okapi")
    okapi_url = "http://%s:%s" % (config["okapi_host"], config["okapi_port"])

    #Start Okapi
    okapi_proc = run_okapi(config["okapi_path"], config["okapi_port"], config["okapi_log"])

    print("Creating tenant %s" % config["tenant"])
    tenant_resp = create_tenant(okapi_url, config["tenant"], "diku", "diku")
    if not tenant_resp.ok:
        print("Got reponse %s creating tenant: %s" % (tenant_resp.status_code,\
                tenant_resp.text))
        okapi_proc.terminate()
        sys.exit(1)

    #Start Modules
    module_install_list = []
    for module_name in config["module_load_list"]:
        print("Loading module %s" % module_name)
        module_dict = config["modules"][module_name]
        try:
            load_module(module_dict=module_dict, okapi_url=okapi_url, \
                    modules_root=config["modules_root"], db_conf=config["db_conf"],\
                    node="localhost", okapi_proc=okapi_proc, tenant=config["tenant"])
        except Exception as e:
            print("Error loading module %s: %s" % (module_name, e))
            okapi_proc.terminate()
            sys.exit(1)
        module_install_list.append( { "id" : module_name, "action" : "enable" } )
    
    try:
        module_loader.install_modules(module_install_list, okapi_url, tenant=config["tenant"],\
                admin_tenant=None, admin_token=None)
    except Exception as e:
        print("Error adding modules to tenant: %s" % e)
        okapi_proc.terminate()
        sys.exit(1)

    #Unload authtoken
    module_unload_list = []
    module_unload_output = None
    for module_name in config["auth_module_load_list"]:
        module_unload_list.append( { "id" : module_name, "action" : "disable" } )
    try:
        module_unload_output = module_loader.install_modules(module_unload_list,\
                okapi_url, tenant=config["tenant"], admin_tenant=None, admin_token=None)
    except Exception as e:
        print("Error unloading modules: %s" % e)
        okapi_proc.terminate()
        sys.exit(1)
    
    #Do Data Loading
    if not args.no_reload:
        for data_dict in config["data_load_list"]:
            try:
                print("Loading data at %s" % data_dict["path"])
                load_data(data_dict["endpoint"], data_dict["path"], okapi_url, config["tenant"])
            except Exception as e:
                print("Error loading data from %s: %s" % (data_dict["endpoint"], e))
                okapi_proc.terminate()
                sys.exit(1)

#    #Start Auth Modules
#    for module_name in config["auth_module_load_list"]:
#        print("Loading module %s" % module_name)
#        module_dict = config["modules"][module_name]
#        try:
#            load_module(module_dict=module_dict, okapi_url=okapi_url, \
#                    modules_root=config["modules_root"], db_conf=config["db_conf"],\
#                    node="localhost", okapi_proc=okapi_proc, tenant=config["tenant"])
#        except Exception as e:
#            print("Error loading module %s: %s" % (module_name, e))
#            okapi_proc.terminate()
#            sys.exit(1)

    for entry in module_unload_output:
        entry["action"] = "enable"
    try:
        module_loader.install_modules(module_unload_output, okapi_url, tenant=config["tenant"],
                admin_tenant=None, admin_token=None)
    except Exception as e:
        print("Error reloading modules: %s" % e)
        okapi_proc.terminate()
        sys.exit(1)

    print("Okapi process is running at %s" % okapi_proc.pid)


