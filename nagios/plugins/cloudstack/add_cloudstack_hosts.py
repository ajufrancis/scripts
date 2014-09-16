#!/usr/bin/python
# coding: utf-8
import CloudStack, pprint, os
import argparse

mhost = {
  'api': 'http://csm01:8080/client/api',
  'apikey': 'f0Q70X5oTpax-b7bvyzDQf2t_rKaK0rWkLXhejPRqI4i6IgiSq5rJ5_KXo7pCE9-HpYqAYllg_Td9675H3E31Q',
  'secret': '8VxNvOkcKn7ibGAQhmI2L8frA7LmdN-IIGXNgmKJ_UxzWTpc487cFLE-vq0yLrXS6-dzL7luNecUyH0elrOA9g',
}

cs = CloudStack.Client(mhost['api'], mhost['apikey'], mhost['secret'])
# Hypervisors
hosts = cs.listHosts({'type': 'Routing'})
#SecondaryStorageVM
ssvms = cs.listHosts({'type': 'SecondaryStorageVM'})
#ConsoleProxy
cpvms = cs.listHosts({'type': 'ConsoleProxy'})
#VirtualRouters
routers = cs.listRouters({'listall': 'True'})


root_folder = '/tmp/cloud'

def add_hosts(hosts):
  for host in hosts:
    tags = ['state_' + host['state']]

    if host['name'].startswith('r-'):
      folder = "VRs/%s/%s" % (host['zonename'], host['account'])
      hostname =  host['name']
      if host['state'] == 'Running':
        tags += [host['hostname']]

    if host['name'].startswith('s-'):
      folder = "SSVMs/%s" % (host['zonename'])
      hostname =  host['name'].split('.')[0]
      tags += [host['podname']]

    if host['name'].startswith('v-'):
      folder = "CPVMs/%s" % (host['zonename'])
      hostname =  host['name']
      tags += [host['podname']]

    if host.has_key('type') and host['type'] == 'Routing':
      folder = "%s/%s/%s" % (host['zonename'], host['podname'], host['clustername'])
      hostname =  host['name']

    tags = '|'.join(tags)
    tags = tags.lower()
    folder_path = "%s/%s" % (root_folder, folder)
    hosts_mk = "%s/%s/hosts.mk" % (root_folder, folder)
    host_data = 'all_hosts += ["%s|wato|%s|/" + FOLDER_PATH + "/",]' % (hostname, tags)

    try:
      os.makedirs(folder_path)
    except os.error:
      pass

    f = open(hosts_mk, 'a')
    f.write(host_data)
    f.write('\n')
    f.close()
    print host_data

def add_dns(hosts):
  for host in hosts:
    dns = ''
    if host.has_key('ipaddress'):
      dns = "%s %s" % (host['ipaddress'], host['name'])
    if host.has_key('publicip'):
      dns = "%s %s" % (host['publicip'], host['name'])
    print dns

add_hosts(cpvms)
add_hosts(ssvms)
add_hosts(routers)
add_hosts(hosts)

#add_dns(cpvms)
#add_dns(ssvms)
#add_dns(hosts)
#add_dns(routers)
