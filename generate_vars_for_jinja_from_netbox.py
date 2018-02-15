import os
import requests
from requests.auth import HTTPBasicAuth
import json
from pprint import pprint
import yaml

def import_variables_from_file():
    my_variables_file=open('variables.yml', 'r')
    my_variables_in_string=my_variables_file.read()
    my_variables_in_yaml=yaml.load(my_variables_in_string)
    my_variables_file.close()
    return my_variables_in_yaml

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_interface(interface_id):
  url = url_base + 'api/dcim/interfaces/' + str(interface_id) + '/'
  rest_call = requests.get(url, headers=headers)
  interface = rest_call.json()['name']
  return interface

my_variables_in_yaml = import_variables_from_file()

url_base = 'http://' + my_variables_in_yaml['ip'] + '/'

token = my_variables_in_yaml['token']

headers={
    'Authorization': 'Token ' + token,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

url = url_base + 'api/dcim/devices/?manufacturer=juniper&is_network_device=True&has_primary_ip=True'

rest_call_get_devices = requests.get(url, headers=headers)

for item in rest_call_get_devices.json()['results']:
    device_name = item['name']
    create_directory(device_name)
    url = url_base + 'api/ipam/ip-addresses/?device=' + device_name
    rest_call_get_device_details = requests.get(url, headers=headers)
    device_details = []
    for item in rest_call_get_device_details.json()['results']:
        address = item['address']
        interface_id = item['interface']['id']
        interface = get_interface(interface_id)
        device_details_item = {'interface': str(interface), 'address':str(address)}
        device_details.append(device_details_item)
        out_file = open(device_name + "/vars_from_netbox_api.yml", "w")
        out_file.write("vars_from_netbox_api:\n")
        out_file.write(yaml.dump(device_details, default_flow_style=False))
        out_file.close()

