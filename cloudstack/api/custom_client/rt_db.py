#!/usr/bin/python
import sys
import MySQLdb
import MySQLdb.cursors

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
  reload(sys)
  sys.setdefaultencoding(default_encoding)

conn = MySQLdb.connect(
    host='127.0.0.1',
        user='root',
        passwd='password',
        db='racktables_db',
        port=3306,
        charset='utf8',
        cursorclass = MySQLdb.cursors.DictCursor
)

cur = conn.cursor()
cur.execute('select * from Object')
data = cur.fetchall()  
cur.close()
conn.close()

vmlist = open('cs_vm.log')
for row in data:
  for key in row.keys():
    row[key] = str(row[key])
  print '%s, %s, %s' % (row['objtype_id'], row['id'], row['name'])

#def insert_obj:
#INSERT INTO `racktables_db`.`Object` (`id`, `name`, `label`, `objtype_id`, `asset_no`, `has_problems`, `comment`) VALUES (NULL, 'test', 'test', '1504', '', 'no', 'test');

#def set_obj_ip:
#INSERT INTO `racktables_db`.`IPv4Allocation` (`object_id`, `ip`, `name`, `type`) VALUES ('770', INET_ATON('192.168.32.1'), 'os-inferface-name', 'ip-type:regular');

vmlist.close()
