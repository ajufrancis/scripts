#!/usr/bin/python
# coding=UTF-8
# http://www.shencan.net/index.php/2013/08/02/saltstack%E4%B9%9D-api%E6%8E%A5%E5%8F%A3/
import salt.grains
import salt.client

# create a local client object
client = salt.client.LocalClient()
ret1 = client.cmd('localpred-01', ['grains.items'],[''])
#ret2 = client.cmd('localpred-01', ['grains.item', 'grains.item', 'grains.item'], [['kernel'], ['os_family'], ['os']])
# make compound execution calls with the cmd method

#'test': {'ipaddress': u'10.24.64.14',
#          'tag_os_fullname': 'centos',
#          'tag_port_tcp': 'tcp_22',
#          'tag_state': 'Running'}

#"test|lan|no_ttl|centos|no_devtype|no_sla|ping|no_cluster|up|cs_fengce|no_pod|Running|no_zone|no_mttf|linux|tcp_22|prod|no_mttr|wato|/" + FOLDER_PATH + "/",

# Explicit IP addresses
#ipaddresses.update({'test': u'10.24.64.14'})

for host in ret1.keys():
  wato_host = ret1[host]['grains.items']
  print wato_host
