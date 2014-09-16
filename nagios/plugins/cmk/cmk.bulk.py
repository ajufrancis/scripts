#!/usr/bin/python

def wato_host(host):
  host['tags'] += ['wato']
  host['tags'] =  '|'.join(host['tags'])
  wato_host = 'all_hosts += ["%s/%s|%s|/" + FOLDER_PATH + "/",]' % (host['folder'], host['name'], host['tags'])
  print wato_host

######################################
# example:
######################################
#host = {
#  'folder': 'cloud',
#  'name': 'i-18-1222-VM',
#  'tags': ['gdupc', 'vm'],
#}
#wato_host(host)
######################################
