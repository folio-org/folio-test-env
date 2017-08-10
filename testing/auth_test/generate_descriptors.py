#!/usr/bin/python3

import argparse
import json
import os
import sys

def generate_descriptor_from_template(module_descriptor_path, template_file_path, template_placeholder="<<<id>>>"):
    #get the id from the module descriptor
    with open(module_descriptor_path, 'r') as module_descriptor_handle:
        module_descriptor_json = json.loads(module_descriptor_handle.read())
        id_name = module_descriptor_json["id"]
        descriptor_parent, template_name = os.path.split(template_file_path)
        descriptor_name_part = os.path.splitext(template_name)[0]
        descriptor_path = os.path.join(descriptor_parent, descriptor_name_part + ".json")
        with open(descriptor_path, 'w') as descriptor_handle:
            with open(template_file_path, 'r') as template_handle:
                template_contents = template_handle.read()
                descriptor_contents = template_contents.replace(template_placeholder, id_name)
                descriptor_handle.write(descriptor_contents)

"""
Batch file is just a json file formatted like the following:
{
    "associations" : [
        {
            "module_descriptor" : "/home/vagrant/mod-users/ModuleDescriptor.json",
            "templates" : [
                "/home/vagrant/folio-test-env/testing/auth_test/deployment_descriptors/mod-users.template",
                "/home/vagrant/folio-test-env/testing/auth_test/tenant_associations/mod-users.template",
            ]
        }
    ]
}
"""
def process_batch_file(batch_file_path, template_placeholder="<<<id>>>"):
    with open(batch_file_path, 'r') as batch_file_handle:
        batch_file_json = json.loads(batch_file_handle.read())
        for association in batch_file_json["associations"]:
            md_path = association["module_descriptor"]
            for template in association["templates"]:
                print("Applying id from MD at %s to template at %s" %\
                        (md_path, template))
                generate_descriptor_from_template(md_path, template, template_placeholder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate descriptors from a module descriptor and template file(s)')
    parser.add_argument('--batch_file_path')
    parser.add_argument('--module_descriptor_path')
    parser.add_argument('--descriptor_template_path', nargs="+")
    args = parser.parse_args()
    if(not args.batch_file_path and \
            (not args.module_descriptor_path or \
            not args.descriptor_template_path)):
        print("You must provide a batch file, or a module descriptor and one or more descriptor templates.")
        sys.exit(1)
    if args.batch_file_path:
        print("Using batch file %s" % args.batch_file_path)
        try:
            process_batch_file(args.batch_file_path)
        except Exception as e:
            print("Error occurred running batch: %s" % e)
            sys.exit(1)

    if args.module_descriptor_path and args.descriptor_template_path:
        for template_path in args.descriptor_template_path:
            print("Generating a descriptor for '%s', using id from '%s'" %\
                (template_path, args.module_descriptor_path))
            try:
                generate_descriptor_from_template(args.module_descriptor_path,\
                    template_path)
            except Exception as e:
                print("Error generating template: %s" % e)
                sys.exit(1)

