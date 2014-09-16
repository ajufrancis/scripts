#!/usr/bin/python
#coding=utf-8
import sys, os
#import active_directory
import salt, CloudStack

#me = active_directory.AD_object ("LDAP://ou=users,dc=hdtr,dc=com")
#for person in active_directory.search (objectCategory='Person'):
#  print person.displayName

def api():
    api = 'http://csm01:8080/client/api'
    #admin
    apikey='f0Q70X5oTpax-b7bvyzDQf2t_rKaK0rWkLXhejPRqI4i6IgiSq5rJ5_KXo7pCE9-HpYqAYllg_Td9675H3E31Q'
    secret='8VxNvOkcKn7ibGAQhmI2L8frA7LmdN-IIGXNgmKJ_UxzWTpc487cFLE-vq0yLrXS6-dzL7luNecUyH0elrOA9g'
    api = CloudStack.Client(api, apikey, secret)
    return api


def list_obj(type):
  request = {
    'listall':'true'
  }
  if type == 'vms':
    return api.listVirtualMachines(request)
  elif type == 'users':
    return api.listAccounts(request)

api = api()
vms = list_obj('vms')
users = list_obj('users')

def ad_add_group(group):
  print group 

def ad_add_groups(groups):
  for name in groups:
    ad_add_group(name)

def ad_add_host(host):
  print host 

def ad_add_hosts(hosts):
  for host in hosts:
    ad_add_host(host)

for vm in vms:
  try:
    ad_add_host(vm['instancename'])
  except:
    pass
