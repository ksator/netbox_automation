
###################################################
# This script generates an Ansible dynamic inventory from Netbox API
###################################################

###################################################
# usage: 
# python ansible_dynamic_inventory.py
# more hosts
###################################################



###################################################
# This block indicates the various imports
###################################################

import requests
from requests.auth import HTTPBasicAuth
import json
from pprint import pprint
import yaml

##################################################
# This block defines the functions we will use
###################################################

def import_variables_from_file():
    my_variables_file=open('variables.yml', 'r')
    my_variables_in_string=my_variables_file.read()
    my_variables_in_yaml=yaml.load(my_variables_in_string)
    my_variables_file.close()
    return my_variables_in_yaml

def get_device_type_id(model):
    url=url_base + 'api/dcim/device-types/?model=' + model
    rest_call = requests.get(url, headers=headers)
    device_type_id = rest_call.json()['results'][0]['id']
    return device_type_id

######################################################
# this block generates the Ansible dynamic inventory from Netbox API
######################################################

my_variables_in_yaml = import_variables_from_file()

url_base = 'http://' + my_variables_in_yaml['ip'] + '/'

token = my_variables_in_yaml['token']

headers={
    'Authorization': 'Token ' + token,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

ansible_inventory_file = open('hosts', "w")

ansible_inventory_file.write("[juniper:children]\n")

url=url_base + 'api/dcim/device-types/?is_network_device=True&manufacturer=juniper'

rest_call = requests.get(url, headers=headers)

for item in rest_call.json()['results']:
   model = item['model']
   ansible_inventory_file.write(model + "\n")
ansible_inventory_file.write("\n")

for item in rest_call.json()['results']:
   model = item['model']
   ansible_inventory_file.write("[" + model+ "]\n")
   device_type_id = get_device_type_id(model)
   url = url_base + 'api/dcim/devices/?manufacturer=juniper&device_type_id=' + str(device_type_id) + '&is_network_device=True&has_primary_ip=True'
   rest_call = requests.get(url, headers=headers)
   for item in rest_call.json()['results']:
       name = item['name']
       ip = item["primary_ip4"]["address"]
       ip = ip.split("/")[0]
       ansible_inventory_file.write(name + " junos_host=" + ip + "\n")
   ansible_inventory_file.write("\n")

url = url_base + 'api/dcim/sites/'
rest_call_get_sites = requests.get(url, headers=headers)
for site in rest_call_get_sites.json()['results']:
    site_name = site['name']
    ansible_inventory_file.write("[" + site_name + "]\n")
    url = url_base + 'api/dcim/devices/?manufacturer=juniper&site=' + site_name + '&is_network_device=True&has_primary_ip=True'
    rest_call_get_devices = requests.get(url, headers=headers)
    for device in rest_call_get_devices.json()['results']:
        device_name = device['name']
        ansible_inventory_file.write(device_name + "\n")
    ansible_inventory_file.write("\n")

url= url_base + 'api/dcim/device-roles/'
rest_call_get_roles = requests.get(url, headers=headers)
for role in rest_call_get_roles.json()['results']:
    role_name = role['name']
    ansible_inventory_file.write("[" + role_name + "]\n")
    url = url_base + 'api/dcim/devices/?manufacturer=juniper&role=' + role_name + '&is_network_device=True&has_primary_ip=True'
    rest_call_get_devices = requests.get(url, headers=headers)
    for device in rest_call_get_devices.json()['results']:
        device_name = device['name']
        ansible_inventory_file.write(device_name + "\n")
    ansible_inventory_file.write("\n")

ansible_inventory_file.close()


