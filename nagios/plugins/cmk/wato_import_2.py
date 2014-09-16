#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#Author: Bastian Kuhn bk@mathias-kettner.de
# enhanced by: Phil Randal phil.randal@gmail.com

#set testing True to output to stdout instead of creating files
#testing = True
testing = False

import os
import sys

# tag mappings
# these correspond to host tags define in WATO

# map each tag dropdown entry to its parent tag
#     or itself if a single checkbox
#     or "" if it is an auxiliary tag

tagz = {
# dropdown tags
   'cmk-agent': 'agent',
   'snmp-only': 'agent',
   'snmp-tcp':  'agent',
   'snmp-v1':  'agent',
   'ping': 'agent',
   
   'prod': 'criticality',
   'critical': 'criticality',
   'test': 'criticality',
   'offline': 'criticality',

   'lan': 'networking',
   'wan': 'networking',
   'dmz': 'networking',

# checkbox tags

   'dns': 'dns',

# auxiliary tags
   
   'snmp': '',
   'tcp': '',

}

try:
    pathlokal = "~/etc/check_mk/conf.d/wato/"
    pathlokal = os.path.expanduser(pathlokal)
    datei = open(sys.argv[1],'r') 
except:
    print """Run this script inside a OMD site
    Usage: ./wato_import.py csvfile.csv
    CSV Example:
    wato_folder_name;host_name;host_alias;parents;ip_address;tag1|tag2"""
    sys.exit()

errorz = 0
folders = {}
for line in datei:
    line=line.replace('\n',';\n')
    ordner, name, alias, parents, ip, tags = line.split(';')[:6]
    if testing == False:
        if ordner:
          try:
            os.makedirs(pathlokal+ordner)
          except os.error:
            pass
    folders.setdefault(ordner,[])

    folders[ordner].append((name,alias,parents,ip,tags))
datei.close()

for folder in folders:
    f_name = folder.split('/')[-1]
    h_num = len(folders[folder])
    f_info = "{'attributes': {}, 'num_hosts': %d, 'title': u'%s'}" % (h_num, f_name)
    f_path = open(pathlokal + folder + '/.wato','w')
    f_path.write(f_info)
    f_path.close()

    all_hosts = "" 
    host_attributes = "" 
    ip_addresses = ""
    alias_details = ""
    parent_details = ""
    for name, alias, parents, ip, tags in folders[folder]:
#      print tags
      tags2 = tags.replace('|\n','')
      all_hosts += "  '%s|%s',\n" % (name, tags2)
      ip_addresses += "  '%s': u'%s',\n" % (name, ip)
      alias_details += "  (u'%s', ['%s']),\n" % (alias, name)
        
      parent_details += "  ('%s', ['%s']),\n" % (parents, name)
		
      host_attributes += "  '%s': {\n" % (name)
      host_attributes += "    'alias': u'%s',\n" % (alias)
      host_attributes += "    'ipaddress': u'%s',\n" % (ip)
      parents2 = parents.replace(",","', '")
      host_attributes += "    'parents': ['%s'],\n" % (parents2)
		
      # handle tags
		
#      words = tags.split("|")
#      for word in words:
#	if tagz.has_key(word):
#	  tg = tagz[word]
#          if tg != "":
#            host_attributes += "    'tag_%s': '%s',\n" % (tg, word)
#        else:
#          if word != "":
#              print ("host '%s' has unrecognised tag '%s'" % (name,word))
#              errorz += 1
      host_attributes = host_attributes[:-2] + "},\n"

#    if errorz != 0:
#      print "Error(s) detected - aborting"
#      sys.exit()
      
    if testing:
        print ('##########################################\n\n# Folder: %s\n\n') % folder

        print ('all_hosts += [')
        print (all_hosts)
        print (']\n\n')
	
        print('# Explicit IP addresses\nipaddresses.update({')
        # {'test': u'127.0.0.1'}
        print (ip_addresses[:-2])
        print ('})\n\n')
	
        print ("# Settings for alias\nextra_host_conf.setdefault('alias', []).extend([")
        # (u'test', ['test')]
        print (alias_details[:-2])
        print ('])\n\n')
    
        print ("# Settings for parents\nextra_host_conf.setdefault('parents', []).extend([")
        # ('test_parent', ['test'])
        print (parent_details[:-2])
        print ('])\n\n')
	
        print ('host_attributes.update({')
        print (host_attributes[:-2])
        print ('})\n')
    else:
        ziel = open(pathlokal + folder + '/hosts.mk','w')

        ziel.write('all_hosts += [')
        ziel.write(all_hosts)
        ziel.write(']\n\n')

        ziel.write('# Explicit IP addresses\nipaddresses.update({')
        # {'test': u'127.0.0.1'}
        ziel.write(ip_addresses[:-2])
        ziel.write('})\n\n')

        ziel.write("# Settings for alias\nextra_host_conf.setdefault('alias', []).extend([")
        # (u'test', ['test')]
        ziel.write(alias_details[:-2])
        ziel.write('])\n\n')

        ziel.write("# Settings for parents\nextra_host_conf.setdefault('parents', []).extend([")
        # ('test_parent', ['test'])
        ziel.write(parent_details[:-2])
        ziel.write('])\n\n')
                                                
        ziel.write('host_attributes.update({')
        ziel.write(host_attributes[:-2])
        ziel.write('})')

        ziel.close()

#    info_file = pathlokal + folder + '.wato'
#    info = open(info_file,'w')
#    {'attributes': {'contactgroups': (True, ['cg_ops']),
#                'parents': ['sw01'],
#                'snmp_community': u'snmp-com-ro',
#                'tag_agent': 'cmk-agent',
#                'tag_criticality': 'prod',
#                'tag_networking': 'lan'},
#'num_hosts': 1,
#    print '\'title\': u\'' + folder + '\''
#    print '{\'attributes\': {}, \'num_hosts\': '
#    print  len(folders[folder])
#    print '}'
#    print(', 'title': u'test'\}')
#    info.close()
