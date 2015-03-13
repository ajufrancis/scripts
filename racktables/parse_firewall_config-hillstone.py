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
