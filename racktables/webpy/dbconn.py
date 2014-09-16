import web

db=web.database(dbn='mysql', db='racktables_db', user='root',host='192.168.11.7',pw='gdcloud.com')
# 查询表
entries = db.select('IPv4Address')

# where 条件
myvar = dict(reserved="yes")
results = db.select('IPv4Address', myvar, where="reserved = yes")
#results = db.select('IPv4Address', where="id>100")

# 查询具体列
#results = db.select('IPv4Address', what="id,name")

# order by
#results = db.select('IPv4Address', order="post_date DESC")

# group
#results = db.select('IPv4Address', group="color")

# limit
#results = db.select('IPv4Address', limit=10)

# offset
#results = db.select('IPv4Address', offset=10)
