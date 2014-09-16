#!/usr/bin/python
# coding=UTF-8
from prettytable import PrettyTable

def print_vms():
    num = 0
    output = []
    vms = list_vms()
    for vm in vms:
        num += 1
        try:
          vm_info = "%s: instancename: %s state: %s name: %s displayname: %s account: %s hostname: %s" % (
            num,
            vm['instancename'],
            vm['state'],
            vm['name'],
            vm['displayname'],
            vm['account'],
            vm['hostname']
        )
          output += [vm_info]
        except Exception, e:
          pass
    return output


# api functions
def pprint_vms():
    x = PrettyTable(["id", 'created', 'state', "instancename", "name", "displayname", "account", 'haenable', 'cpunumber','memory'])
# 'macaddress', 'ipaddress', hostname'
# 'zonename', 'podname', 'clustername'
    x.align["created"] = "l"
    x.align["state"] = "l"
    x.align["instancename"] = "l"
    x.align["name"] = "l"
    x.align["displayname"] = "l"
    x.align["account"] = "l"
    x.align["memory"] = "l"
    x.align["name"] = "l"
    x.align["publicip"] = "l"
    x.align["displayname"] = "l"
    x.padding_width = 1

    # add vm's properties to array
    id = 0
    vms = list_vms()
    for vm in vms:
      id += 1
      # if vm state is stopped, some properties not exist
      vm['memory'] = MB_to_GB(vm['memory'])
      try:
        values = [ id, vm['created'], vm['state'], vm['instancename'], vm['name'], vm['displayname'], vm['account'], vm['haenable'], vm['cpunumber'], vm['memory']]
        x.add_row(values)
 #     print values
      except:
        pass

    print x
