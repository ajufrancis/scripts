#!/usr/bin/python
import CloudStack

api = 'http://192.168.11.2:8080/client/api'
#admin
apikey='f0Q70X5oTpax-b7bvyzDQf2t_rKaK0rWkLXhejPRqI4i6IgiSq5rJ5_KXo7pCE9-HpYqAYllg_Td9675H3E31Q'
secret='8VxNvOkcKn7ibGAQhmI2L8frA7LmdN-IIGXNgmKJ_UxzWTpc487cFLE-vq0yLrXS6-dzL7luNecUyH0elrOA9g'

cs_object = CloudStack.Client(api, apikey, secret)
#zones = cs_object.listZones()
capacity = cs_object.listCapacity()

#print 'instancename,created,state,haenable,id,name,displayname,cpunumber,cpuspeed,memory,mac,ip,publicip,domain,domainid,zonename,zoneid,hypervisor,account,hostname,hostid,serviceofferingname'

for data in capacity:
  #for key in data.keys():
  #  print key,
  #  print type(data[key]),
  #  print data[key]
  print data
