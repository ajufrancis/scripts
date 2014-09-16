#!/usr/bin/python
import CloudStack

api = 'http://192.168.11.2:8080/client/api'
#admin
apikey='f0Q70X5oTpax-b7bvyzDQf2t_rKaK0rWkLXhejPRqI4i6IgiSq5rJ5_KXo7pCE9-HpYqAYllg_Td9675H3E31Q'
secret='8VxNvOkcKn7ibGAQhmI2L8frA7LmdN-IIGXNgmKJ_UxzWTpc487cFLE-vq0yLrXS6-dzL7luNecUyH0elrOA9g'

cs_object = CloudStack.Client(api, apikey, secret)
hosts = cs_object.listHosts()

#for key in hosts[0].keys():
#  print key + ',',
#print '\n'
# print key,type(host[key])

for host in hosts:
  if host.has_key('hypervisor'):
    for key in host.keys():
      if isinstance(host[key],unicode):
        print host[key].encode('utf-8') + ',',
      else:
        print str(host[key]) + ',',
    print
