#!/usr/bin/python
import CloudStack
import simplejson as json

def listVMs():
  api = 'http://csm01:8080/client/api'
  #admin
  apikey='f0Q70X5oTpax-b7bvyzDQf2t_rKaK0rWkLXhejPRqI4i6IgiSq5rJ5_KXo7pCE9-HpYqAYllg_Td9675H3E31Q'
  secret='8VxNvOkcKn7ibGAQhmI2L8frA7LmdN-IIGXNgmKJ_UxzWTpc487cFLE-vq0yLrXS6-dzL7luNecUyH0elrOA9g'
  data = {}
  cs_object = CloudStack.Client(api, apikey, secret)
  vms = cs_object.listVirtualMachines({ 'listall':'true' })
  data['total'] = len(vms)
  data['rows'] = vms
  return data

data = listVMs()
print json.dumps(data)
