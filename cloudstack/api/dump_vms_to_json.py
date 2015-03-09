#!/usr/bin/python
import CloudStack
import simplejson as json

def dump_vms():
  api = 'http://csm01:8080/client/api'
  #admin
  apikey='f0Q70X5oTpax-b7bvyzDQf2t_rKaK0rWkLXhejPRqI4i6IgiSq5rJ5_KXo7pCE9-HpYqAYllg_Td9675H3E31Q'
  secret='8VxNvOkcKn7ibGAQhmI2L8frA7LmdN-IIGXNgmKJ_UxzWTpc487cFLE-vq0yLrXS6-dzL7luNecUyH0elrOA9g'
  data = {}
  cs_object = CloudStack.Client(api, apikey, secret)
  vms = cs_object.listVirtualMachines({ 'listall':'true' })

  all_vms = []
  for vm in vms:
      for nic in vm['nic']:
          if nic['type'] == 'Shared':
              vm['ip'] = nic['ipaddress']
              vm['mac'] = nic['macaddress']

      all_vms += [vm]

  data['total'] = len(all_vms)
  data['rows'] = all_vms
  print json.dumps(all_vms)

# start here
dump_vms()
