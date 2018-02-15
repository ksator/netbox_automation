## Documentation structure
[**About Netbox**](README.md#about-netbox)  
[**About this repo**](README.md#about-this-repo)  
[**How to use this repo**](README.md#how-to-use-this-repo)    
[**Netbox Installation**](README.md#netbox-installation)  
[**install the requirements to use the automation content hosted in this repository**](README.md#install-the-requirements-to-use-the-automation-content-hosted-in-this-repository)  
[**clone this repository**](README.md#clone-this-repository)  
[**Define your variables**](README.md#define-your-variables)  
[**Configure Netbox with automation**](README.md#configure-netbox-with-automation)  
[**Delete Netbox configuration with automation**](README.md#delete-netbox-configuration-with-automation)  
[**Looking for more automation solutions**](README.md#looking-for-more-automation-solutions)  


## About Netbox

Netbox is a popular open source IP address management (IPAM) and data center infrastructure management (DCIM) tool maintained by Jeremy Stretch.  

Netbox has RESTful API. The NetBox API represents all objects in JSON.  
There is a NAPALM integration to pull some data from devices for validation purpose. 

Here's the [doc](https://netbox.readthedocs.io/en/latest/)   
Here's the [code](https://github.com/digitalocean/netbox)  

## About this repo

This repository uses Python to: 

- Automation content to configure an existing Netbox server
- Automation content to generate a dynamic ansible inventory from Netbox API
- Automation content to  generate yaml variables for Jinja templates from Netbox API

This repository doesnt install Netbox. You still need to install Netbox yourself.

This repository has been tested using: 
- Ubuntu 16.04
- Python 2.7
- Netbox v2.2.9
    
## How to use this repo

The steps are:  
- Install Netbox. This repository doesnt install Netbox. You still need to install Netbox yourself.  
- Install the requirements to use the python scripts hosted in this repository  
- Clone this repository
- Edit the file [**variables.yml**](variables.yml) to indicate what you want to configure on Netbox
- Execute the script [**configure_netbox.py**](configure_netbox.py): It uses the variables defined in the file [**variables.yml**](variables.yml) and configure Netbox    

## Netbox Installation
See the [**installation guide**](http://netbox.readthedocs.io/en/stable/)  
This repository has been tested with Netbox version v2.2.9  

Once netbox is installed, you can use it: 
- netbox GUI http://your_netbox_server
- netbox API http://your_netbox_server/api/
- netbox API doc http://your_netbox_server/api/docs/

This repository use Netbox REST API. So you need to create a Netbox API Token. 


## install the requirements to use the automation content hosted in this repository  
The python scripts  hosted in this repository use the library **requests** to makes REST calls to Netbox.   
Run these commands on your laptop:
```
sudo -s
pip install requests
```

## clone this repository
Run these commands on your laptop:
```
sudo -s
git clone https://github.com/ksator/netbox_automation.git 
cd netbox_automation
```

## Define your variables

The file [**variables.yml**](variables.yml) defines variables.
On your laptop, edit it to indicate details such as:
- The IP address of your Netbox server
- The Netbox user token you want to use
- The Netbox details you want to configure with automation: 
   - a tenant
   - sites
   - device-roles
   - devices
   - prefixes-roles
   - prefixes
   - device management ip addresses
   - ip addresses to assign to devices interfaces
   - interface connections (physical topology) 
   - In addition to this, there are others Netbox details that will be configured automatically: 
     - device-types (Juniper qfx5100-48s-6q and qfx10002-36q) 
     - a platform (Junos platform with a junos napalm_driver)

Run these commands on your laptop:
```
vi variable.yml
```
```
$ more variables.yml 
---
# Edit this file to define the details to configure on Netbox

# netbox server ip @
ip: 192.168.233.152

# netbox user token you want to use
token: 'b1b0f72bed6946d352b78781030e8d626f5e8c28'

# netbox tenants you want to create. please create one single tenant.
tenants: 
    - evpn-vxlan-demo

# netbox sites you want to create. the sites are assigned to the tenant.
sites:
    - dc1
    - dc2

# netbox device-roles you want to create
device-roles: 
    - "spine_switch"
    - "leaf_switch"   

# device-types qfx5100-48s-6q and qfx10002-36q are automatically created. 
# interface_templates are automatically created for device-types qfx5100-48s-6q and qfx10002-36q
# power_port_templates are automatically created for device-types qfx5100-48s-6q and qfx10002-36q
# Juniper Junos platform is be automatically created with a junos napalm_driver

# prefix roles you want to create
prefix_roles: 
    - out_of_band_management
    - devices_interconnection

# prefixes you want to create. 
# These prefixes are assigned to the tenant.
prefixes:
    - prefix: 10.0.2.0/24
      role: devices_interconnection
    - prefix: 172.25.90.0/24
      role: out_of_band_management
    
# devices you want to create. the devices are assigned to the tenant.
devices: 
    - name: QFX5100-183
      device_type: qfx5100-48s-6q
      device_role: leaf_switch
      site: dc1
    - name: QFX5100-186
      device_type: qfx5100-48s-6q
      device_role: leaf_switch
      site: dc1
    - name: QFX10K2-178
      device_type: qfx10002-36q
      device_role: spine_switch
      site: dc1
    - name: QFX10K2-180
      device_type: qfx10002-36q
      device_role: spine_switch
      site: dc1
    - name: QFX10K2-181
      device_type: qfx10002-36q
      device_role: spine_switch
      site: dc1
    - name: QFX10K2-174
      device_type: qfx10002-36q
      device_role: spine_switch
      site: dc2
    - name: QFX10K2-175
      device_type: qfx10002-36q
      device_role: spine_switch
      site: dc2
    
# management ip addresses you want to create. the IP addresses are assigned to the tenant.
management_addresses: 
    - ip: 172.25.90.183
      device: QFX5100-183
      interface: vme0
      mgmt_only: True
    - ip: 172.25.90.186
      device: QFX5100-186
      interface: vme0
      mgmt_only: True
    - ip: 172.25.90.178
      device: QFX10K2-178
      interface: em0
      mgmt_only: True
    - ip: 172.25.90.174
      device: QFX10K2-174
      interface: em0
      mgmt_only: True
    - ip: 172.25.90.175
      device: QFX10K2-175
      interface: em0
      mgmt_only: True
    - ip: 172.25.90.180
      device: QFX10K2-180
      interface: em0
      mgmt_only: True
    - ip: 172.25.90.181
      device: QFX10K2-181
      interface: em0
      mgmt_only: True

# Other ip addresses you want to create. the IP addresses are assigned to the tenant.
ip_addresses:
    - ip: 10.0.2.13/31
      device: QFX10K2-180
      interface: et-0/0/0
    - ip: 10.0.2.23/31
      device: QFX10K2-180
      interface: et-0/0/1
    - ip: 10.0.2.15/31
      device: QFX10K2-181
      interface: et-0/0/0
    - ip: 10.0.2.25/31
      device: QFX10K2-181
      interface: et-0/0/1
    - ip: 10.0.2.9/31
      device: QFX10K2-178
      interface: et-0/0/0
    - ip: 10.0.2.19/31
      device: QFX10K2-178
      interface: et-0/0/1

# define how the interfaces are connected (physical topology). 
interface_connections:
    - device_a: QFX5100-183
      interface_a: et-0/0/48
      device_b: QFX10K2-178
      interface_b: et-0/0/2
      connection_status: Connected
    - device_a: QFX10K2-181
      interface_a: et-0/0/3
      device_b: QFX5100-186
      interface_b: et-0/0/49
      connection_status: Connected
```
## Configure Netbox with automation

The script [**configure_netbox.py**](configure_netbox.py) configure Netbox using the file [**variables.yml**](variables.yml) 

```
$ python configure_netbox.py 
device role spine_switch successfully created
device role leaf_switch successfully created
tenant evpn-vxlan-demo successfully created
site dc1 successfully created
site dc2 successfully created
device type qfx5100-48s-6q successfully created
device type qfx10002-36q successfully created
prefix role out_of_band_management successfully created
prefix role devices_interconnection successfully created
prefix 10.0.2.0/24 successfully created
prefix 172.25.90.0/24 successfully created
platform junos with a junos napalm_driver successfully created
device QFX5100-183 successfully created
device QFX5100-186 successfully created
device QFX10K2-178 successfully created
device QFX10K2-180 successfully created
device QFX10K2-181 successfully created
device QFX10K2-174 successfully created
device QFX10K2-175 successfully created
address ip 172.25.90.183 successfully created
address ip 172.25.90.186 successfully created
address ip 172.25.90.178 successfully created
address ip 172.25.90.174 successfully created
address ip 172.25.90.175 successfully created
address ip 172.25.90.180 successfully created
address ip 172.25.90.181 successfully created
address ip 10.0.2.13/31 successfully created
address ip 10.0.2.23/31 successfully created
address ip 10.0.2.15/31 successfully created
address ip 10.0.2.25/31 successfully created
address ip 10.0.2.9/31 successfully created
address ip 10.0.2.19/31 successfully created
interface connection between QFX5100-183 et-0/0/48 and QFX10K2-178 et-0/0/2 successfully created
interface connection between QFX10K2-181 et-0/0/3 and QFX5100-186 et-0/0/49 successfully created

```
## Delete Netbox configuration with automation
The script [**delete_netbox_configuration.py**](delete_netbox_configuration.py) delete the Netbox configuration: 
   - all tenants
   - all sites
   - all device-roles
   - all device-types
   - all platforms
   - all interface connections
   - all devices
   - all prefixes-roles
   - all prefixes
   - all ip addresses
```
$ python delete_netbox_configuration.py 
```

## Looking for more automation solutions

https://github.com/ksator?tab=repositories  
https://gitlab.com/users/ksator/projects  
https://gist.github.com/ksator/  

