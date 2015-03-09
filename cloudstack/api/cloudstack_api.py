#!/usr/bin/python
# coding: UTF-8
import CloudStack
import sys, os

#http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
def MB_to_GB(num):
  if num < 1024.0:
    return "%sMB" % num
  num /= 1024.0
  return "%2.1f%s" % (num, 'GB')

def get_publicip_info(ipaddress):
#http://download.cloud.com/releases/3.0.3/api_3.0.3/root_admin/listPublicIpAddresses.html
  request = { 
    'listall': 'true',
    'allocatedonly': 'true',
    'ipaddress': ipaddress
  }
  return api.listPublicIpAddresses(request)

def get_fw_rules(ipaddress):
# http://download.cloud.com/releases/3.0.3/api_3.0.3/root_admin/listFirewallRules.html
  ip = get_publicip_info(ipaddress)
  request = {
    'listall': 'true',
    'ipaddressid': ip['publicipaddress'][0]['id']
  }
  return api.listFirewallRules(request)
   
def print_fw_rules(ipaddress):
  rules = []
  for r in get_fw_rules(ipaddress):
    try:
      rules += [ "from: %s to: %s %s-%s" % (r['cidrlist'], r['protocol'], r['startport'], r['endport']) ]
    except:
      rules += [ "from: %s to: %s icmptype: %s icmpcode: %s" % (r['cidrlist'], r['protocol'], r['icmptype'], r['icmpcode']) ]
  print rules

#def net_disassociate_publicip()
#def delete_fw_nat()

# url maps to api
urls = ('/client', 'client')

def api():
    api = 'http://csm01:8080/client/api'
    #admin
    apikey='f0Q70X5oTpax-b7bvyzDQf2t_rKaK0rWkLXhejPRqI4i6IgiSq5rJ5_KXo7pCE9-HpYqAYllg_Td9675H3E31Q'
    secret='8VxNvOkcKn7ibGAQhmI2L8frA7LmdN-IIGXNgmKJ_UxzWTpc487cFLE-vq0yLrXS6-dzL7luNecUyH0elrOA9g'
    api = CloudStack.Client(api, apikey, secret)
    return api
  

def list_vms():
#http://download.cloud.com/releases/3.0.3/api_3.0.3/root_admin/listVirtualMachines.html
    request = {
      'listall':'true'
     }
    return api.listVirtualMachines(request)

class client:
  def GET(self):
    return vms_info

def run_web():
  if __name__ == "__main__":
    import web
    vms_info = print_vms()
    app = web.application(urls, globals())
    app.run()
