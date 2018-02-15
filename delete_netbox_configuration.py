###################################################
# This script deletes almost all the netbox configuration
###################################################

###################################################
# usage: python delete_netbox_configuration.py
###################################################



###################################################
# This block indicates the various imports
###################################################
import requests
from requests.auth import HTTPBasicAuth
import json
from pprint import pprint
import yaml
import time


##################################################
# This block defines the functions we will use
###################################################

def import_variables_from_file():
 my_variables_file=open('variables.yml', 'r')
 my_variables_in_string=my_variables_file.read()
 my_variables_in_yaml=yaml.load(my_variables_in_string)
 my_variables_file.close()
 return my_variables_in_yaml

my_variables_in_yaml = import_variables_from_file()

url_base = 'http://' + my_variables_in_yaml['ip'] + '/'

token = my_variables_in_yaml['token']

headers={
    'Authorization': 'Token ' + token,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def delete_ip_addresses():
 url=url_base + 'api/ipam/ip-addresses'
 rest_call = requests.get(url, headers=headers)
 for item in rest_call.json()['results']:
  id=item['id']
  url=url_base + 'api/ipam/ip-addresses/' + str(id) + '/'
  rest_call = requests.delete(url, headers=headers)

def delete_interface_connections(): 
    url=url_base + 'api/dcim/interface-connections/'
    rest_call = requests.get(url, headers=headers)
    for item in rest_call.json()['results']:
       id=item['id']
       url=url_base + 'api/dcim/interface-connections/' + str(id) + '/'
       rest_call = requests.delete(url, headers=headers)


######################################################

def delete_devices():
 url=url_base + 'api/dcim/devices'
 rest_call = requests.get(url, headers=headers)
 for item in rest_call.json()['results']:
  id=item['id']
  url=url_base + 'api/dcim/devices/' + str(id) + '/'
  rest_call = requests.delete(url, headers=headers)

def delete_device_types():
 url=url_base + 'api/dcim/device-types'
 rest_call = requests.get(url, headers=headers)
 for item in rest_call.json()['results']:
  id=item['id']
  url=url_base + 'api/dcim/device-types/' + str(id) + '/'
  rest_call = requests.delete(url, headers=headers)

def delete_prefixes():
 url=url_base + 'api/ipam/prefixes'
 rest_call = requests.get(url, headers=headers)
 for item in rest_call.json()['results']:
  id=item['id']
  url=url_base + 'api/ipam/prefixes/' + str(id) + '/'
  rest_call = requests.delete(url, headers=headers)

def delete_sites():
 url=url_base + 'api/dcim/sites'
 rest_call = requests.get(url, headers=headers)
 for item in rest_call.json()['results']:
  id=item['id']
  url=url_base + 'api/dcim/sites/' + str(id) + '/'
  rest_call = requests.delete(url, headers=headers)

def delete_tenants():
 url=url_base + 'api/tenancy/tenants'
 rest_call = requests.get(url, headers=headers)
 for item in rest_call.json()['results']:
  id=item['id']
  url=url_base + 'api/tenancy/tenants/' + str(id) + '/'
  rest_call = requests.delete(url, headers=headers)

def delete_device_role():
 url=url_base + 'api/dcim/device-roles'
 rest_call = requests.get(url, headers=headers)
 for item in rest_call.json()['results']:
  id=item['id']
  url=url_base + 'api/dcim/device-roles/' + str(id) + '/'
  rest_call = requests.delete(url, headers=headers)

def delete_prefix_roles():
  url=url_base + 'api/ipam/roles'
  rest_call = requests.get(url, headers=headers)
  for item in rest_call.json()['results']:
   id=item['id']
   url=url_base + 'api/ipam/roles/' + str(id) + '/'
   rest_call = requests.delete(url, headers=headers)

def delete_platforms():
  url=url_base + 'api/dcim/platforms'
  rest_call = requests.get(url, headers=headers)
  for item in rest_call.json()['results']:
   id=item['id']
   url=url_base + 'api/dcim/platforms/' + str(id) + '/'
   rest_call = requests.delete(url, headers=headers)


######################################################
# this block deletes almost all the Netbox configuration
######################################################

delete_ip_addresses()

delete_interface_connections()

delete_devices()

delete_prefixes()

delete_sites()

delete_device_types()

delete_tenants()

delete_device_role()

delete_prefix_roles()

delete_platforms()
