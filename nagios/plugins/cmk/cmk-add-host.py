#!/usr/bin/python

f = open('gdupc-vm.log')
vms = f.readlines()
for vm in vms:
  name = vm.split(' ')[0]
  print 'all_hosts += ["%s|wato|/" + FOLDER_PATH + "/",]' % name
for vm in vms:
  name = vm.split(' ')[0]
  alias = vm.split(' ')[1]
  print "host_attributes.update({'%s': {'alias': '%s'}})" % (name, alias)
f.close()
