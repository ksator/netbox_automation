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
         print 'device role ' + item + ' successfully created'
     else:
         print 'failed to create device role ' + item

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
         print 'tenant ' + item + ' successfully created'
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

def get_platform_id(platform):
 url=url_base + 'api/dcim/platforms/?name=' + platform
 rest_call = requests.get(url, headers=headers)
 #pprint (rest_call.json())
 #if rest_call.status_code != 200:
 #    print 'failed to get the id of the platform ' + platform
 platform_id = rest_call.json()['results'][0]['id']
 #print platform_id
 return platform_id

def create_platform():
 url=url_base + 'api/dcim/platforms/'
 payload={
     "napalm_driver": "junos",
     'name': 'junos',
     'rpc_client': 'juniper-junos',
     'slug': 'junos'
 }
 rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
 #pprint (rest_call.json())
 if rest_call.status_code == 201:
     print 'platform junos successfully created'
 else:
     print 'failed to create platform junos'

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
         print 'site ' + item + ' successfully created'
     else:
         print 'failed to create site ' + item

def get_site_id(site):
 url=url_base + 'api/dcim/sites/?name=' + site
 rest_call = requests.get(url, headers=headers)
 #pprint (rest_call.json())
 #if rest_call.status_code != 200:
 #    print 'failed to get the id of the site ' + site
 site_id = rest_call.json()['results'][0]['id']
 #print site_id
 return site_id

def create_device_types():
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
            print 'device type ' + item['model'] + ' successfully created'
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

def create_prefix_roles():
    url=url_base + 'api/ipam/roles/'
    for item in my_variables_in_yaml['prefix_roles']:
     payload={
         "name": item,
         "slug": item
     }
     rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
     #pprint (rest_call.json())
     if rest_call.status_code == 201:
         print 'prefix role ' + item + ' successfully created'
     else:
         print 'failed to create prefix role ' + item

def get_prefix_role_id(prefix_role):
    url=url_base + 'api/ipam/roles/?name=' + prefix_role
    rest_call = requests.get(url, headers=headers)
    #pprint (rest_call.json())
    #if rest_call.status_code != 200:
    #    print 'failed to get the id of the prefix_role ' + prefix_role
    prefix_role_id = rest_call.json()['results'][0]['id']
    #print prefix_role_id
    return prefix_role_id

def create_prefixes():
    url=url_base + 'api/ipam/prefixes/'
    for item in my_variables_in_yaml['prefixes']:
     payload={
           "prefix": item['prefix'],
           "tenant": get_tenant_id(my_variables_in_yaml['tenants'][0]),
           "status": 1,
           "role": get_prefix_role_id(item['role'])
     }
     rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
     #pprint (rest_call.json())
     if rest_call.status_code == 201:
         print 'prefix ' + item['prefix'] + ' successfully created'
     else:
         print 'failed to create prefix ' + item['prefix']

def create_devices():
    url=url_base + 'api/dcim/devices/'
    for item in my_variables_in_yaml['devices']:
     payload={
           "name": item['name'],
           "device_type": get_device_type_id(item['device_type']),
           "status": 1,
           "device_role": get_device_role_id(item['device_role']),
           "platform": get_platform_id('junos'),
           "site": get_site_id(item['site']),
           "tenant": get_tenant_id(my_variables_in_yaml['tenants'][0])
     }
     rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
     #pprint (rest_call.json())
     if rest_call.status_code == 201:
         print 'device ' + item['name'] + ' successfully created'
     else:
         print 'failed to create device ' + item['name']

def get_device_details(device):
  device_id=get_device_id(device)
  url=url_base + 'api/dcim/devices/' + str(device_id)
  rest_call = requests.get(url, headers=headers)
  # print url
  # pprint(rest_call.json())
  name=rest_call.json()['name']
  device_type=rest_call.json()['device_type']['id']
  status=rest_call.json()['status']['value']
  device_role=rest_call.json()['device_role']['id']
  platform=rest_call.json()['platform']['id']
  site=rest_call.json()['site']['id']
  tenant=rest_call.json()['tenant']['id']
  id=rest_call.json()['id']
  payload={
           "name": name,
           "device_type": device_type,
           "status": status,
           "device_role": device_role,
           "platform": platform,
           "site": site,
           "tenant": tenant
  }
  #print payload
  return payload

def create_ip_addresses():
    url=url_base + 'api/ipam/ip-addresses/'
    for item in my_variables_in_yaml['addresses']:
     device=item['device']
     interface=item['interface']
     payload={
           "status": 1,
           "address": item['ip'],
           "tenant": get_tenant_id(my_variables_in_yaml['tenants'][0]),
           "interface": get_interface_id(interface, device)
     }
     rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
     #pprint (rest_call.json())
     if rest_call.status_code == 201:
         print 'address ip ' + item['ip'] + ' successfully created'
     else:
         print 'failed to create ip address ' + item['ip']

def create_management_ip_address():
    for item in my_variables_in_yaml['addresses']:
     if item['mgmt_only']==True:
      device_id=get_device_id(item['device'])
      interface_id=get_interface_id(item['interface'], item['device'])
      address_id=get_address_id((item['device']), interface_id)
      url=url_base + 'api/dcim/devices/' + str(device_id) + '/'
      payload={
          "primary_ip4": address_id
      }
      #print device_id
      #print interface_id
      #print address_id
      #print url
      #print payload
      rest_call = requests.patch(url, headers=headers, data=json.dumps(payload))
      #pprint (rest_call.json())

def get_address_id(device, interface_id):
    url=url_base + 'api/ipam/ip-addresses/?device=' + device + '&interface_id=' + str(interface_id)
    rest_call = requests.get(url, headers=headers)
    #pprint (rest_call.json())
    #if rest_call.status_code != 200:
    #    print 'failed to get the address id for device ' + device + ' and interface_id ' + interface_id
    address_id = rest_call.json()['results'][0]['id']
    #print "address_id is " + str(address_id)
    return address_id

def get_device_id(device):
    url=url_base + 'api/dcim/devices/?name=' + device
    rest_call = requests.get(url, headers=headers)
    #pprint (rest_call.json())
    #if rest_call.status_code != 200:
    #    print 'failed to get the id of the device ' + device
    device_id = rest_call.json()['results'][0]['id']
    #print "device_id is " + str(device_id)
    return device_id

def get_interface_id(interface, device):
    url=url_base + 'api/dcim/interfaces/?name=' + interface + '&device=' + device
    rest_call = requests.get(url, headers=headers)
    #pprint (rest_call.json())
    #if rest_call.status_code != 200:
    #    print 'failed to get the id of the interface ' + interface + ' of the device ' + device
    interface_id = rest_call.json()['results'][0]['id']
    #print "interface_id is " + str(interface_id)
    return interface_id


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
#for item in my_variables_in_yaml['sites']:
#    get_site_id(item)

create_device_types()
#get_device_type_id('qfx10002-36q')
#get_device_type_id('qfx5100-48s-6q')
#for item in ['qfx5100-48s-6q','qfx10002-36q']:
#    get_device_type_id(item)

create_interface_templates_for_qfx5100_48s_6q()
create_interface_templates_for_qfx10002_36q()

for item in ['qfx5100-48s-6q','qfx10002-36q']:
    create_power_port_templates(item)

create_prefix_roles()

for item in my_variables_in_yaml['prefix_roles']:
   get_prefix_role_id(item)

create_prefixes()

#get_platform_id('Juniper Junos')
#get_platform_id('junos')

create_platform()

create_devices()

create_ip_addresses()

create_management_ip_address()

#get_device_details('QFX5100-183')
