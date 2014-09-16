#!/usr/bin/python
import CloudStack
import sys

#inventory tcp/udp port
#inventory services port
#if os:windows or port rdp inventory tcp
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

api = 'http://192.168.11.2:8080/client/api'
#admin
apikey='f0Q70X5oTpax-b7bvyzDQf2t_rKaK0rWkLXhejPRqI4i6IgiSq5rJ5_KXo7pCE9-HpYqAYllg_Td9675H3E31Q'
secret='8VxNvOkcKn7ibGAQhmI2L8frA7LmdN-IIGXNgmKJ_UxzWTpc487cFLE-vq0yLrXS6-dzL7luNecUyH0elrOA9g'

cs_object = CloudStack.Client(api, apikey, secret)
vms = cs_object.listVirtualMachines({ 'listall':'true' })
keys = [
'nic',
'templateid',
'hostid',
'publicipid',
'rootdeviceid',
'templatedisplaytext',
'domainid',
'securitygroup',
'zoneid',
'passwordenabled',
'id',
'guestosid',
'serviceofferingid',
]

#def set_tag_agent:
#  if g_tag_conf['agent']
#def set_wato_hostname:
#  if g_use_dns

for vm in vms:
  wato = {}
  wato['foldername'] = vm['domain'] + '/' + vm['zonename'] + '/' + vm['account']
  wato['hostname'] = vm['instancename']
  wato['alias'] = vm['displayname']
  wato['parent'] = 'sw01'

# wato_folder = {
#    'permission': 'account',
#    'hostname': 'dns',
#    'agent': 'cmk-agent',
#    'parent': 'sw01',
#  }
# wato_default['dns']
# wato['template'] = 
#  wato['icons'] = folder
#  wato['hostgroups']
#  wato['servicegroups']

  tag = {}
  tag['agent'] = 'ping'
  tag['crit'] = 'offline'
  tag['network'] = 'lan'
  tag['wato'] = 'wato'
#  tag['name'] = vm['name']
#  tag['virttype'] = vm['hypervisor']


  wato['ip'] = vm.get('publicip','LOSTIP')
#  try:
#    tag['hostname'] = vm['hostname']
#  except KeyError:
#    tag['hostname'] = vm.setdefault('hostname', 'LOSTNAME')
#    tag['hostname'] = vm.get('hostname','LOSTNAME')

#  tag['haenable'] = str(vm['haenable'])
#  tag['created'] = vm['created']
#  tag['state'] = vm['state']
#  tag['templatename'] = vm['templatename']
#  tag['serviceofferingname'] = vm['serviceofferingname']
#  host_extinfo['cpunumber']
#  host_extinfo['cpuused']
#  host_extinfo['memory']
#  host_extinfo['macaddress']
#  host_extinfo['ip']
#  host_extinfo['rootdevicetype']
#  host_extinfo['rootdevice']
#  host_extinfo['datadevices']
#  host_extinfo['networkkbsread']
#  host_extinfo['networkkbswrite']
#  host_extinfo['cpuspeed']

#  if tag['agent'] = 'snmp_v2':
#    wato['snmp_com'] = 'snmp-com-ro' 

  wato['tags'] = '|'.join(tag.values())
#  print ';'.join(wato.values())
  print '%s;%s;%s;%s;%s;%s' % (wato['foldername'], wato['hostname'],wato['alias'], wato['parent'], wato['ip'], wato['tags'])
