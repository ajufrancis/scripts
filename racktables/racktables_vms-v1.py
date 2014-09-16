#!/usr/bin/python
#import CloudStack
import sys
import MySQLdb
import MySQLdb.cursors
import time

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
  reload(sys)
  sys.setdefaultencoding(default_encoding)

conn=MySQLdb.connect(host='192.168.11.7',db='racktables_db',user='nagios01',passwd='nagios01',port=3306)
cur=conn.cursor()

def ip2int(ip):
  import struct,socket
  return struct.unpack("!I",socket.inet_aton(ip))[0]
def name2id(name):
  sql = "SELECT id FROM  `Object` WHERE object_name = %s" % name
  result = cur.execute(sql)
  if result == 1:
    id = cur.fetchone()[0]
    return id
def get_ip(name)
  id = name2id(name)
  sql = "SELECT inet_ntoa(ip) FROM  `IPv4Allocation` WHERE object_id = %s" % id
  n = cur.execute(sql)
  if n == 1:
    ip = cur.fetchone()
    return ip
        


try:
    f=open('SG-6000.cfg')
    content = f.readlines()
    f.close()

    for line in content:
      if re.search(r'.*dnatrule id.*', line):
        if '10.' in line:
          line = line.replace('dnatrule', '').strip()
          line = line.replace('"', '').strip()

          dnat = {}
          list = line.split(' ')
          if 'port' not in line:
            dnat['id'] = list[1]
            dnat['from'] = list[3]
            dnat['to'] = list[5]
            dnat['trans-to'] = list[7]
          else:
            dnat['id'] = list[1]
            dnat['from'] = list[3]
            dnat['to'] = list[5]
            dnat['service'] = list[7]
            dnat['trans-to'] = list[9]
            dnat['port'] = list[11]

      name = line[0]
      ip = line[1]

#      sql = "SELECT %s FROM  `Object` WHERE name = '%s'" % ('id', name)
      sql = "SELECT object_id FROM  `IPv4Allocation` WHERE ip = inet_aton('%s')" % ip
      n = cur.execute(sql)
      if n == 1:
        id = cur.fetchone()[0]
        sql_select_ip = "SELECT * FROM  `IPv4Allocation` WHERE object_id = %d and ip = INET_ATON('%s')" % (id, ip)
        result = cur.execute(sql_select_ip)
      if result == 0:
	ip = ip2int(ip)
        sql_insert_ip = "INSERT INTO IPv4Allocation (object_id, ip, name, type) VALUES ('%s', '%s', '', 'regular')" % (id, ip)
        n = cur.execute(sql_insert_ip)
	print n

except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])

cur.close()
conn.commit()
conn.close()
