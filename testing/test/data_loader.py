import argparse
import requests
import json
import re
import os
import sys

def grab_id(lookup_path, content_element, okapi_url, token, tenant):
    """
    Make a request to an Okapi path in order to get a listing of items and, if
    it is a unique item, get the id of the item
    """
    headers = {}
    headers["X-Okapi-Token"] = token
    headers["X-Okapi-Tenant"] = tenant
    headers["content-type"] = "application/json"

    r = requests.get(okapi_url + lookup_path, headers=headers)
    
    if r.status_code != 200:
        raise Exception("Bad status code %s on id lookup at url %s: %s" %\
                (r.status_code, okapi_url + lookup_path, r.text))
    content_list = r.json()[content_element]
    if len(content_list) == 0:
        raise Exception("No elements found for url %s" % okapi_url + lookup_path)
    if len(content_list) > 1:
        raise Exception("Multiple elements found for url %s" % okapi_url + lookup_path)

    return content_list[0]["id"]
    
def expand_templates(data_dict, okapi_url, token, tenant):
    """
    Look for values that match the <<content_element|/url_to_content_listing>> format
    and call the grab_id method to look up the actual values for them
    """
    new_dict = data_dict.copy()
    pattern = r"<<(.+)\|(.+)>>"
    for k,v in data_dict.items():
        if type(v) == type(""):
            #print("Attempting to match '%s' against pattern '%s'" % \
            #        (v, pattern))
            match = re.match(pattern, v)
            if not match:
                continue
            content_element = match.group(1)
            lookup_path = match.group(2)
            new_dict[k] = grab_id(lookup_path, content_element, okapi_url, token, tenant)
        if type(v) == type([]):
            new_list = v.copy()
            for i in range(len(new_list)):
                item = new_list[i]
                if type(item) != type(""):
                    continue
                match = re.match(pattern, item)
                if not match:
                    continue
                new_item = grab_id(match.group(2), match.group(1), okapi_url, token, tenant)
                new_list[i] = new_item
            new_dict[k] = new_list
        else:
            continue

    return new_dict


def send_data(data_dict, okapi_url, endpoint, token, tenant):
    """
    Actually POST the new record
    """
    headers = {}
    headers["X-Okapi-Token"] = token
    headers["X-Okapi-Tenant"] = tenant
    headers["Content-Type"] = "application/json"
    r = requests.post(okapi_url + endpoint, headers=headers, json=data_dict)

    if r.status_code != 201:
        raise Exception("Error POSTing data to url %s. Got status %s: %s" %\
                (okapi_url + endpoint, r.status_code, r.text))


def load_file(file_path, okapi_url, endpoint, token, tenant):
    """
    Read a json file in from the disk, expand any microformatted entries and then
    attempt to create it on the CRUD endpoint
    """
    print("Processing file %s" % file_path)
    with open(file_path, 'r') as file_handle:
        json_data = json.load(file_handle)
        expanded_json_data = expand_templates(json_data, okapi_url, token, tenant)
        send_data(expanded_json_data, okapi_url, endpoint, token, tenant)


def load_directory(dir_path, okapi_url, endpoint, token, tenant):
    """
    Grab all .json files in the directory and attempt to upload them to the given
    endpoint
    """
    for filename_raw in os.listdir(dir_path):
        filename = os.fsdecode(filename_raw)
        if filename.endswith(".json"):
            try:
                load_file(os.path.join(dir_path, filename), okapi_url,
                        endpoint, token, tenant)
            except Exception as e:
                raise Exception("Error loading file %s: %s" %\
                        (os.path.join(dir_path, filename), e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Load a directory or single file into an Okapi module')
    parser.add_argument('--okapi_url', default='http://localhost:9130')
    parser.add_argument('--module_endpoint', required=True)
    parser.add_argument('--tenant', default='diku')
    parser.add_argument('--token', default=None)
    parser.add_argument('path')
    args = parser.parse_args()
    path = os.path.abspath(args.path)
    if os.path.isdir(path):
        load_directory(path, args.okapi_url, args.module_endpoint, args.token, args.tenant)
    else:
        load_file(path, args.okapi_url, args.module_endpoint, args.token, args.tenant)


