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

conn = MySQLdb.connect(
    host='192.168.11.7',
        user='nagios01',
        passwd='nagios01',
        db='racktables_db',
        port=3306,
        charset='utf8',
        cursorclass = MySQLdb.cursors.DictCursor
)

sql="SELECT id FROM Object WHERE name = '%s'" % "i-22-1895-VM"
print sql
try:
  cur=conn.cursor()
  output = cur.execute(sql)
  print output
except MySQLdb.Error,e:
  print "MySQL Error %d: %s" % (e.args[0], e.args[1])
cur.close()
conn.commit()
conn.close()
