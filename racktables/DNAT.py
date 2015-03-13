#!/usr/bin/env python
#
import pprint
from ip_vrouter import *

def read_dnat_rule(file):
  f=open(file)
  content = f.readlines()
  f.close()

  ret = []
  for dnatrule in content:
    dnat = {}
    if re.search(r'.*dnatrule id.*', dnatrule):
      dnatrule = dnatrule.replace('dnatrule', '').strip()
      dnatrule = dnatrule.replace('log', '').strip()
      dnatrule = dnatrule.replace('track-ping', '').strip()
      dnatrule = dnatrule.replace('"', '').strip()
      dnatrule = dnatrule.split(' ')
      for i in range(0, len(dnatrule)):
        if dnatrule[i] == 'id':
          dnat['id'] = dnatrule[i+1]
        if dnatrule[i] == 'from':
          dnat['from'] = dnatrule[i+1]
        if dnatrule[i] == 'to':
          dnat['to'] = dnatrule[i+1]
        if dnatrule[i] == 'trans-to':
          dnat['trans-to'] = dnatrule[i+1]
        if dnatrule[i] == 'port':
          dnat['port'] = dnatrule[i+1]
        if dnatrule[i] == 'track-tcp':
          dnat['track-tcp'] = dnatrule[i+1]
      dnat_list += [dnat,]
  return dnat_list

file = '/tmp/config.0'

pp = pprint.PrettyPrinter()
dict = read_ip_vrouter(file)
pp.pprint(dict)
