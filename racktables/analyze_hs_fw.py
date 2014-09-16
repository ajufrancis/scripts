#!/usr/bin/python
# -*- coding: utf-8 -*- 
import pexpect, sys, os, re, datetime
import sys
import MySQLdb
import MySQLdb.cursors
import time

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
  reload(sys)
  sys.setdefaultencoding(default_encoding)

timestamp = "\n######" + datetime.datetime.now().strftime("%Y-%m-%d-%H:%M") + "######\n"

#conn=MySQLdb.connect(host='192.168.11.7',db='racktables_db',user='nagios01',passwd='nagios01',port=3306)
#cur=conn.cursor()
#conn.commit()
#cur.close()

def get_dnat(file):
  f=open(file)
  content = f.readlines()
  f.close()
  
  dnat_list = []
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

def ip2int(ip):
  import struct,socket
  return struct.unpack("!I",socket.inet_aton(ip))[0]
def name2id(name):
  sql = "SELECT id FROM  `Object` WHERE object_name = %s" % name
  result = cur.execute(sql)
  if result == 1:
    id = cur.fetchone()[0]
    return id
def get_ip(name):
  id = name2id(name)
  sql = "SELECT inet_ntoa(ip) FROM  `IPv4Allocation` WHERE object_id = %s" % id
  n = cur.execute(sql)
  if n == 1:
    ip = cur.fetchone()
    return ip

dnat_rules = get_dnat('SG-6000.cfg')
for rule in dnat_rules:
  print rule

#INSERT INTO `racktables_db`.`IPv4Allocation` (`object_id`, `ip`, `name`, `type`) VALUES ('36', INET_ATON('10.24.56.1'), 'nagios', 'regular');
#dnat_info = get_dnat()
#print dnat_info
#for ip in dnat_info['to']:
#  print ip
#  insert_sql = "INSERT INTO `racktables_db`.`IPv4Allocation` (`object_id`, `ip`, `name`, `type`) VALUES ('%d', INET_ATON('ip'), '', 'regular')" % ('1465', ip)
#  print insert_sql
#  result = cur.execute(insert_sql)
#  print result

