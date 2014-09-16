#!/usr/bin/python
import CloudStack

api = 'http://192.168.11.2:8080/client/api'
#admin
apikey='f0Q70X5oTpax-b7bvyzDQf2t_rKaK0rWkLXhejPRqI4i6IgiSq5rJ5_KXo7pCE9-HpYqAYllg_Td9675H3E31Q'
secret='8VxNvOkcKn7ibGAQhmI2L8frA7LmdN-IIGXNgmKJ_UxzWTpc487cFLE-vq0yLrXS6-dzL7luNecUyH0elrOA9g'

cs_object = CloudStack.Client(api, apikey, secret)
hosts = cs_object.listHosts()

#hosts = cs_object.listHosts({'name':'xs229'})


def list_hypervisors():
  keys = ['cpuwithoverprovisioning','version','memorytotal','zoneid','cpunumber','managementserverid','lastpinged','memoryused','id','networkkbswrite','suitableformigration','clusterid','capabilities','state','memoryallocated','cpuused','cpuspeed','type','events','zonename','podid','clustertype','hahost','cpuallocated','ipaddress','name','networkkbsread','created','clustername','hypervisor','islocalstorageactive','resourcestate','hosttags','podname']
  print 'cpuwithoverprovisioning,version,memorytotal,zoneid,cpunumber,managementserverid,lastpinged,memoryused,id,networkkbswrite,suitableformigration,clusterid,capabilities,state,memoryallocated,cpuused,cpuspeed,type,events,zonename,podid,clustertype,hahost,cpuallocated,ipaddress,name,networkkbsread,created,clustername,hypervisor,islocalstorageactive,resourcestate,hosttags,podname'
  for host in hosts:
    host_values = []
# list compute hosts only : hypervisor
    if host['type'] == 'Routing':
      for key in keys():
        if isinstance(host[key],unicode):
	  value = host[key].encode('utf-8') 
        else:
# if value is type of: int or boolean
	  value = str(host[key])
	host_values.append(value)
    if host_values: 
      print '|'.join(host_values)

def list_test():
  i = 0
  for host in hosts:
    if host['type'] == 'Routing':
#    print '|'.join(host.keys())
      print host['name'] + ',' + host['ipaddress'] + ',' + host['clustername']

list_test()
#list_hypervisors()
