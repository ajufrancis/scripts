#!/usr/bin/python
from xml.etree import ElementTree  
#import cs_var.txt

root = ElementTree.parse(r"listVirtualmachines-all.log")

for vm in root.findall('virtualmachine'):
    alias = vm.find('name').text
    name = vm.find('instancename').text
    id = vm.find('id').text
    disname = vm.find('displayname').text

    nic = vm.find('nic')
    ip = nic.find('ipaddress').text 
    mac = nic.find('macaddress').text 

    account = vm.find('account').text
    haenable = vm.find('haenable').text
    created = vm.find('created').text
    state = vm.find('state').text
    cpunum = vm.find('cpunumber').text
    memory = vm.find('memory').text
    hyperv = vm.find('hypervisor').text
    serviceofferingname = vm.find('serviceofferingname').text
    publicip = ""

    networking = "lan"
    agent = "ping"

    if vm.find('publicip') != None :
        publicip = vm.find('publicip').text
    if state.strip('\n') != 'Stopped' :
    	criticality = "prod"
    else :
    	criticality = "offline"

    tags = agent + "|" + criticality + "|" + networking
    root_dir = 'vm/' + account.strip('\n')
    parents = "sw01"
    print root_dir + ";"+name.strip('\n')+";"+alias.strip('\n')+";" + parents + ";" + publicip.strip('\n')+";" + tags

