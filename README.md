## Documentation structure
[**About Netbox**](README.md#about-netbox)  
[**About this repo**](README.md#about-this-repo)  
[**How to use this repo**](README.md#how-to-use-this-repo)    
[**Netbox Installation**](README.md#netbox-installation)  
[**install the requirements to use the automation content hosted in this repository**](README.md#install-the-requirements-to-use-the-automation-content-hosted-in-this-repository)  
[**clone this repository**](README.md#clone-this-repository)  

## About Netbox

Netbox is a popular open source IP address management (IPAM) and data center infrastructure management (DCIM) tool.  
Here's the [doc](https://netbox.readthedocs.io/en/latest/)   
Here's the [code](https://github.com/digitalocean/netbox)  

## About this repo

This repository uses Python to: 

- configure an existing Netbox setup
- get data from Netbox and generate dynamic ansible inventory
- get data from Netbox and generate yaml variables for Jinja templates

This repository doesnt install Netbox. You still need to install Netbox yourself.

## How to use this repo

The steps are:  
- Install Netbox. This repository doesnt install Netbox. You still need to install Netbox yourself.  
- Install the requirements to use the python scripts hosted in this repository  
- Clone this repository
- Edit the file [**variables.yml**](variables.yml) to indicate what you want to configure on Netbox
- Execute the script [**configure_netbox.py**](configure_netbox.py): It uses the variables defined in the file [**variables.yml**](variables.yml) and configure Netbox    

## Netbox Installation
See the [**installation guide**](http://netbox.readthedocs.io/en/stable/)

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



