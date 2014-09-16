#!/usr/bin/python
import CloudStack

api = 'http://192.168.11.2:8080/client/api'
#admin
apikey='f0Q70X5oTpax-b7bvyzDQf2t_rKaK0rWkLXhejPRqI4i6IgiSq5rJ5_KXo7pCE9-HpYqAYllg_Td9675H3E31Q'
secret='8VxNvOkcKn7ibGAQhmI2L8frA7LmdN-IIGXNgmKJ_UxzWTpc487cFLE-vq0yLrXS6-dzL7luNecUyH0elrOA9g'

cs_object = CloudStack.Client(api, apikey, secret)
caps = cs_object.listCapacity()

#CAPACITY_TYPE_MEMORY = 0
# CAPACITY_TYPE_CPU = 1
# CAPACITY_TYPE_STORAGE = 2
# CAPACITY_TYPE_STORAGE_ALLOCATED = 3
# CAPACITY_TYPE_VIRTUAL_NETWORK_PUBLIC_IP = 4
# CAPACITY_TYPE_PRIVATE_IP = 5
# CAPACITY_TYPE_SECONDARY_STORAGE = 6
# CAPACITY_TYPE_VLAN = 7
# CAPACITY_TYPE_DIRECT_ATTACHED_PUBLIC_IP = 8
# CAPACITY_TYPE_LOCAL_STORAGE = 9.
#capacityused
#capacitytotal
#percentused
#zoneid
#type
#zonenamecapacityused
#capacitytotal
#percentused
#zoneid
#type
#zonename

for i in caps['capacity']:
  if i['type'] == 0:
    print "%s memory: capacityused %s capacitytotal:%s percentused:%s" % (i['zonename'],i['capacityused'],i['capacitytotal'],i['percentused'])
  if i['type'] == 1:
    print "%s cpu: capacityused %s capacitytotal:%s percentused:%s" % (i['zonename'],i['capacityused'],i['capacitytotal'],i['percentused'])
  if i['type'] == 2:
    print "%s cstorage: apacityused %s capacitytotal:%s percentused:%s" % (i['zonename'],i['capacityused'],i['capacitytotal'],i['percentused'])
