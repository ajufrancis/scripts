#!/usr/bin/python
import CloudStack, re, sys
import HTML

def get_vms():
  api = 'http://csm01:8080/client/api'
  #admin
  apikey='f0Q70X5oTpax-b7bvyzDQf2t_rKaK0rWkLXhejPRqI4i6IgiSq5rJ5_KXo7pCE9-HpYqAYllg_Td9675H3E31Q'
  secret='8VxNvOkcKn7ibGAQhmI2L8frA7LmdN-IIGXNgmKJ_UxzWTpc487cFLE-vq0yLrXS6-dzL7luNecUyH0elrOA9g'
  cs_object = CloudStack.Client(api, apikey, secret)
  vms = cs_object.listVirtualMachines({ 'listall':'true' })
  return vms

def print_vm_info(vms):
  header = ['No', 'state', 'instancename', 'created', 'haenable', 'id', 'name', 'cpunumber', 'cpuspeed', 'memory', 'macaddress', 'ipaddress', 'domainid', 'zoneid', 'account', 'hostname', 'publicip', 'serviceofferingname']
  num = 0
  for vm in vms:
    try:
      vm['hostname'] = vm['hostname'].encode('utf-8')
      vm['publicip'] = vm['publicip'].encode('utf-8')
#      vm['displayname'] = vm['displayname'].encode('utf-8')
      vm['name'] = vm['name'].encode('utf-8')
      vm['domain'] = vm['domain'].encode('utf-8')
      vm['zonename'] = vm['zonename'].encode('utf-8')
      vm['serviceofferingname'] = vm['serviceofferingname'].encode('utf-8')
      num += 1
      print num, vm['state'],vm['instancename'],vm['created'],vm['haenable'],vm['id'],vm['name'],vm['cpunumber'],vm['cpuspeed'],vm['memory'],vm['nic'][0]['macaddress'],vm['nic'][0]['ipaddress'],vm['domainid'],vm['zoneid'],vm['account'],vm['hostname'],vm['publicip'],vm['serviceofferingname']
    except:
      pass

vms = get_vms()
print_vm_info(vms)
