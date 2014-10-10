#!/usr/bin/python
import json
execfile('./cloudstack.py')

def get_vms_record():
    accounts = cloud.listUsers()
    for account in accounts:
        name = account['account']
        print '{0:#^20}'.format(name)
        request = {'listall': '', 'account': 'fengce' }
        vms = cloud.api.listVirtualMachines(request)
        for vm in vms:
            if vm['state'] =='Running':
                try:
                    ip = vm['publicip']
                except:
                    for network in vm['nic']:
                        if network['type'] == 'Shared':
                            ip = network['ipaddress']

                print '{0} {1} {2}'.format(ip, vm['instancename'], vm['displayname'])

def listUsersVM(name):
    request = {'listall': '', 'account': name }
    vms = cloud.api.listVirtualMachines(request)
    return vms

def vms_to_json(account):
    name = account['account']
    vms = listUsersVM(name)
    print json.dumps(vm)

cloud = cloud()
accounts = cloud.listUsers()
print json.dumps(cloud.listDomains(), indent=4)
