#!/usr/bin/python
# coding=UTF-8
# http://www.shencan.net/index.php/2013/08/02/saltstack%E4%B9%9D-api%E6%8E%A5%E5%8F%A3/
import salt.grains
import salt.client

print salt.grains.core.hostname()

def wato_host():
  host = {
#    'name': __grains__['fqdn'],
    'alias': '',
#    'ipaddr': __grains__['ipv4'],
    'parent': []
  }
  

def defgw(host):
  client = salt.client.LocalClient()
  ret = client.cmd(host, 'cmd.run', ['ip route'])
  routes = ret.values()[0]
  routes = routes.split('\n')
  defgw = routes[-1].split(' ')[2]
  return defgw
