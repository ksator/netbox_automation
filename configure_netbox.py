###################################################
# This script takes the variables defined in the file variables.yml and make rest calls to Netbox to configure it.
###################################################

###################################################
# usage: python configure_netbox.py
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
 # print my_variables_in_string
 my_variables_in_yaml=yaml.load(my_variables_in_string)
 # print my_variables_in_yaml
 # print my_variables_in_yaml['ip']
 my_variables_file.close()
 return my_variables_in_yaml

def create_device_roles():
 url=url_base + 'api/dcim/device-roles/'
 for item in my_variables_in_yaml['device-roles']:
     payload={
         "name": item,
         "slug": item,
         "color": "2196f3"
     }
     rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
     #pprint (rest_call.json())
     if rest_call.status_code == 201:
         print item + ' device-roles created'
     else:
         print 'failed to create device-roles ' + item

def get_device_role_id(role):
 url=url_base + 'api/dcim/device-roles/?name=' + role
 rest_call = requests.get(url, headers=headers)
 #pprint (rest_call.json())
 #if rest_call.status_code != 200:
 #    print 'failed to get the id of the role ' + role
 role_id = rest_call.json()['results'][0]['id']
 #print role_id
 return role_id

def create_tenants():
 url=url_base + 'api/tenancy/tenants/'
 for item in my_variables_in_yaml['tenants']:
     payload={
         "name": item,
         "slug": item
     }
     rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
     #pprint (rest_call.json())
     if rest_call.status_code == 201:
         print item + ' tenant created'
     else:
         print 'failed to create tenant ' + item

def get_tenant_id(tenant):
 url=url_base + 'api/tenancy/tenants/?name=' + tenant
 rest_call = requests.get(url, headers=headers)
 #pprint (rest_call.json())
 #if rest_call.status_code != 200:
 #    print 'failed to get the id of the tenant ' + tenant
 tenant_id = rest_call.json()['results'][0]['id']
 #print tenant_id
 return tenant_id

def get_manufacturer_id(manufacturer):
 url=url_base + 'api/dcim/manufacturers/?name=' + manufacturer
 rest_call = requests.get(url, headers=headers)
 #pprint (rest_call.json())
 #if rest_call.status_code != 200:
 #    print 'failed to get the id of the manufacturer ' + manufacturer
 manufacturer_id = rest_call.json()['results'][0]['id']
 #print manufacturer_id
 return manufacturer_id

def create_sites():
 url=url_base + 'api/dcim/sites/'
 tenant_id=get_tenant_id(my_variables_in_yaml['tenants'][0])
 for item in my_variables_in_yaml['sites']:
     payload={
         "name": item,
         "slug": item,
         "tenant": tenant_id
     }
     rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
     #pprint (rest_call.json())
     if rest_call.status_code == 201:
         print item + ' site created'
     else:
         print 'failed to create site ' + item

def device_types():
    url=url_base + 'api/dcim/device-types/'
    Juniper_id=get_manufacturer_id('Juniper')
    device_types_list=[{"manufacturer": Juniper_id, "model": "qfx5100-48s-6q", "slug": "qfx5100-48s-6q", "part_number": "650-049938", "u_height": 1, "is_full_depth": True, "is_network_device": True},{ "manufacturer": Juniper_id, "model": "qfx10002-36q", "slug": "qfx10002-36q", "part_number": "750-059497", "u_height": 2, "is_full_depth": True, "is_network_device": True}]
    for item in device_types_list:
        payload={
        "manufacturer": item['manufacturer'],
        "model": item['model'],
        "slug": item['slug'],
        "part_number": item['part_number'],
        "u_height": item['u_height'],
        "is_full_depth": item ["is_full_depth"],
        "is_network_device": item["is_network_device"]
        }
        rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
        #pprint (rest_call.json())
        if rest_call.status_code == 201:
            print item['model'] + ' device type created'
        else:
            print 'failed to create device type ' + item['model']

def get_device_type_id(model):
    url=url_base + 'api/dcim/device-types/?model=' + model
    rest_call = requests.get(url, headers=headers)
    #pprint (rest_call.json())
    #if rest_call.status_code != 200:
    #    print 'failed to get the id of the device_type ' + model
    device_type_id = rest_call.json()['results'][0]['id']
    #print device_type_id
    return device_type_id

def create_interface_templates_for_qfx5100_48s_6q():
    url=url_base + 'api/dcim/interface-templates/'
    for item in range (0, 47): 
        payload={
            "device_type": get_device_type_id('qfx5100-48s-6q'),
            "name": "xe-0/0/" + str(item),
            "form_factor": 1200,
            "mgmt_only": False
        }
        rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
        #pprint (rest_call.json())
    for item in range (48, 53): 
        payload={
            "device_type": get_device_type_id('qfx5100-48s-6q'),
            "name": "et-0/0/" + str(item),
            "form_factor": 1400,
            "mgmt_only": False
        }
        rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
        #pprint (rest_call.json())
    payload={
        "device_type": get_device_type_id('qfx5100-48s-6q'),
        "name": "vme0",
        "form_factor": 1000,
        "mgmt_only": True
    }
    rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
    #pprint (rest_call.json())

def create_power_port_templates(model):
     url=url_base + 'api/dcim/power-port-templates/'
     for item in ['Power Supply 0','Power Supply 1']:
        payload={
            "device_type": get_device_type_id(model),
            "name": item
        }
        rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
        #pprint (rest_call.json())


def create_interface_templates_for_qfx10002_36q():
    url=url_base + 'api/dcim/interface-templates/'
    for item in range (0, 31): 
        payload={
            "device_type": get_device_type_id('qfx10002-36q'),
            "name": "et-0/0/" + str(item),
            "form_factor": 1400,
            "mgmt_only": False
        }
        rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
        #pprint (rest_call.json())
    payload={
        "device_type": get_device_type_id('qfx10002-36q'),
        "name": "em0",
        "form_factor": 1000,
        "mgmt_only": True
    }
    rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
    #pprint (rest_call.json())



######################################################
# this block is the Netbox configuration using REST calls
######################################################

my_variables_in_yaml=import_variables_from_file()
url_base = 'http://' + my_variables_in_yaml['ip'] + '/'
token = my_variables_in_yaml['token']
headers={
    'Authorization': 'Token ' + token,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

create_device_roles()
#for item in my_variables_in_yaml['device-roles']: 
#    get_device_role_id(item)

create_tenants()
#get_tenant_id(my_variables_in_yaml['tenants'][0])

create_sites()

device_types()
#get_device_type_id('qfx10002-36q')
#get_device_type_id('qfx5100-48s-6q')
#for item in ['qfx5100-48s-6q','qfx10002-36q']:
#    get_device_type_id(item)

create_interface_templates_for_qfx5100_48s_6q()
create_interface_templates_for_qfx10002_36q()

for item in ['qfx5100-48s-6q','qfx10002-36q']:
    create_power_port_templates(item)




