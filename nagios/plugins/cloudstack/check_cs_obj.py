#!/usr/bin/python
import CloudStack

api = 'http://192.168.11.2:8080/client/api'
#admin
apikey='f0Q70X5oTpax-b7bvyzDQf2t_rKaK0rWkLXhejPRqI4i6IgiSq5rJ5_KXo7pCE9-HpYqAYllg_Td9675H3E31Q'
secret='8VxNvOkcKn7ibGAQhmI2L8frA7LmdN-IIGXNgmKJ_UxzWTpc487cFLE-vq0yLrXS6-dzL7luNecUyH0elrOA9g'

cs = CloudStack.Client(api, apikey, secret)
csm
zones = cs.listZones()
pods = cs.listPods()
clusters = cs.listClusters()
hosts = cs.listHosts()
capacitys = cs.listCapacity()
routers = cs.listRouters()
svms = cs.listSystemVms()
vms = cs.listVirtualMachines({ 'listall':'true' })

def check_zones():
  for zone in zones:
    print '<<<%s>>>' % zone['name']
    print zone['allocationstate']

def check_pods():
  for pod in pods:
    print '<<<%s>>>' % pod['name']
    print pod['allocationstate']

def check_clusters():
  for cluster in clusters:
    print '<<<%s>>>' % cluster['name']
    print cluster['allocationstate']

def check_hosts():
  for host in hosts:
    print '<<<%s>>>' % host['name']
    print host['state']

def check_routers():
  for router in routers:
    print '<<<%s>>>' % router['name']
    print router['state']

def check_svms():
  for svm in svms:
    print '<<<%s>>>' % svm['name']
    print svm['state']

#def check_capacitys():
#  for capacity in capacitys:
#    print '<<<%s>>>' % capacity['name']
#    print capacity['state']
#    print type(capacity)
    #print capacity['type']
    #print capacity['zonename']
#    for key in capacity.keys():
#      print key,capacity[key]

def check_vms():
  for vm in vms:
    print '<<<%s>>>' % vm['name']
    print vm['state']

#check_zones()
#check_pods()
#check_clusters()
#check_hosts()
#check_routers()
#check_svms()
#check_capacitys()
check_vms()
