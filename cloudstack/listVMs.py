#!/usr/bin/python
import re, sys
import HTML, json

execfile('./get_dnat_ip.py')
execfile('./cloudstack.py')

def print_vm_table(vms):
  t = HTML.Table(header_row=['state', 'instancename', 'created', 'haenable', 'id', 'name', 'cpunumber', 'cpuspeed', 'memory', 'macaddress', 'ipaddress', 'domainid', 'zoneid', 'account', 'hostname', 'publicip', 'nat_ip', 'serviceofferingname'])
  for vm in vms:
    try:
      vm['hostname'] = vm['hostname'].encode('utf-8')
      vm['publicip'] = vm['publicip'].encode('utf-8')
#      vm['displayname'] = vm['displayname'].encode('utf-8')
      vm['name'] = vm['name'].encode('utf-8')
      vm['domain'] = vm['domain'].encode('utf-8')
      vm['zonename'] = vm['zonename'].encode('utf-8')
      vm['serviceofferingname'] = vm['serviceofferingname'].encode('utf-8')

      vm['nat_ip'] = ''
      for i in get_dnat_ip(vm['publicip']):
        vm['nat_ip'] += "<li>%s</li>" % i
      vm['nat_ip'] = "<ul>%s</ul>" % vm['nat_ip']
      t.rows.append([vm['state'],vm['instancename'],vm['created'],vm['haenable'],vm['id'],vm['name'],vm['cpunumber'],vm['cpuspeed'],vm['memory'],vm['nic'][0]['macaddress'],vm['nic'][0]['ipaddress'],vm['domainid'],vm['zoneid'],vm['account'],vm['hostname'],vm['publicip'],vm['nat_ip'],vm['serviceofferingname']])
    except:
      pass

  htmlcode = str(t)
  print htmlcode

cloud = cloud()
vms = list_vms()
print_vm_table(vms)
