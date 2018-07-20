import argparse
import sys
import requests
import os
import json

def get_headers(tenant, token=None, content_type="application/json"):
    headers = {}
    if tenant:
        headers["X-Okapi-Tenant"] = tenant
    if token:
        headers["X-Okapi-Token"] = token
    headers["Content-Type"] = content_type

def send_module_descriptor(okapi_url, module_descriptor, admin_tenant, admin_token=None):
    headers = get_headers(admin_tenant, admin_token)
    response = requests.post(okapi_url + "/_/proxy/modules", headers=headers,\
            json=module_descriptor)
    if not response.ok:
        raise Exception("Error posting module descriptor for %s: %s" %\
                (module_descriptor["id"], response.text))

def send_deployment_descriptor(okapi_url, deployment_descriptor, admin_tenant, admin_token):
    headers = get_headers(admin_tenant, admin_token)
    response = requests.post(okapi_url + "/_/discovery/modules", headers=headers,\
            json=deployment_descriptor)
    if not response.ok:
        raise Exception("Error posting deployment descriptor for %s: %s" %\
                (deployment_descriptor["srvcId"], response.text))

def add_module_to_tenant(okapi_url, module_id, tenant, admin_tenant, admin_token):
    headers = get_headers(admin_tenant, admin_token)
    url = okapi_url + "/_/proxy/tenants/%s/modules" % tenant
    response = requests.post(url, headers=headers, json={"id" : module_id})
    if not response.ok:
        raise Exception("Error posting to URL %s, Got code %s adding module to tenant %s: %s" %\
                (url, response.status_code, tenant, response.text))
    

def load_module(okapi_url, module_descriptor, deployment_descriptor, tenant,\
        admin_tenant, admin_token=None):
    send_module_descriptor(okapi_url=okapi_url, module_descriptor=module_descriptor,\
            admin_tenant=admin_tenant, admin_token=admin_token)
    send_deployment_descriptor(okapi_url=okapi_url, deployment_descriptor=deployment_descriptor,\
            admin_tenant=admin_tenant, admin_token=admin_token)
    add_module_to_tenant(okapi_url=okapi_url, module_id=module_descriptor["id"],\
            tenant=tenant, admin_tenant=admin_tenant, admin_token=admin_token)

def make_deployment_descriptor(module_id, exec_string, url, node_id):
    dd = {}
    dd["srvcId"] = module_id
    dd["nodeId"] = node_id
    descriptor = {}
    dd["descriptor"] = descriptor
    if exec_string:
        descriptor["exec"] = exec_string
    if url:
        descriptor["url"] = url
    return dd

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Register, deploy and add a module to a tenant')
    parser.add_argument('--okapi_url', default='http://localhost:9130')
    parser.add_argument('--tenant', default='diku')
    parser.add_argument('--admin_token', default=None)
    parser.add_argument('--admin_tenant', default=None)
    parser.add_argument('--exec_string', default=None)
    parser.add_argument('--url', default=None)
    parser.add_argument('--node_id', default='localhost')
    parser.add_argument('module_descriptor_path')
    args = parser.parse_args()

    if not( bool(args.exec_string) != bool(args.url) ):  #Exclusive or
        print("You must specify EITHER an exec_string OR a url for deployment")
        sys.exit(1)

    module_descriptor = None
    try:
        abs_md_path = os.path.abspath(args.module_descriptor_path)
        with open(abs_md_path, 'r') as md_handle:
            module_descriptor = json.load(md_handle)
            if not module_descriptor:
                raise Exception("No json returned from parsing %s" % abs_md_path)
            if not 'id' in module_descriptor.keys():
                raise Exception("No id in module descriptor json")
    except Exception as e:
        print("Unable to read module descriptor from %s: %s" % (abs_md_path, e))
        sys.exit(1)

    deployment_descriptor = make_deployment_descriptor(module_descriptor["id"], args.exec_string,\
            args.url, args.node_id)
    
    try:
        load_module(okapi_url=args.okapi_url, module_descriptor=module_descriptor,\
                deployment_descriptor=deployment_descriptor, tenant=args.tenant,\
                admin_tenant=args.admin_tenant, admin_token=args.admin_token)
    except Exception as e:
        print("Error loading module %s: %s" % (module_descriptor["id"], e))
        sys.exit(1)
