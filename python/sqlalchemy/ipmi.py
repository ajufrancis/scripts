#!/usr/bin/python
#coding:utf-8
import sqlalchemy
from sqlalchemy.orm import mapper, sessionmaker
from datetime import datetime
from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, String, Unicode, DateTime
#创建到数据库的连接,echo=True 表示用logging输出调试结果
engine = sqlalchemy.create_engine('mysql+mysqlconnector://root:gdcloud.com@localhost:3306/test')

#跟踪表属性
metadata = MetaData()
#创建一个表所需的信息:字段,表名等
table_ipmi = Table(
    'tf_ipmi', metadata,
    Column('uuid', Integer, primary_key=True, nullable=False, default=0),
    Column('minion_id', Unicode(255), unique=True),
    Column('mac_addr', Unicode(255), unique=True, default=''),
    Column('ip_src', Unicode(255), unique=False, nullable=False),
    Column('ip_adr', Unicode(255), unique=True),
    Column('defgw_mac', Unicode(255), unique=False),
    Column('defgw_ip', Unicode(255), unique=False),
    Column('subnet_mask', Unicode(255), unique=False),
    Column('snmp_community', Unicode(255), unique=False, default='public'),
    Column('created', DateTime, default=datetime.now)
)

#在数据库中生成表
metadata.create_all(engine)
#创建一个映射类
class IPMI(object): pass
#把表映射到类
mapper(IPMI, table_ipmi)

#sessionmaker() 函数是最常使用的创建最顶层可用于整个应用 Session 的方法,Session 管理着所有与数据库之间的会话
Session = sessionmaker()
#将创建的数据库连接关联到这个session
Session.configure(bind=engine)
#创建了一个自定义了的 Session类
session = Session()

u = IPMI()
u.minion_id='xstest2'
u.mac_addr='dongwm@dongwm.com'
u.defgw_mac='dongwm@dongwm.com'
u.defgw_ip='dongwm@dongwm.com'
u.mac_addr='dongwm@dongwm.com'
u.ip_src='dongwm@dongwm.com'
u.ip_addr='dongwm@dongwm.com'
u.subnet_mask='dongwm@dongwm.com'
#给映射类添加以下必要的属性,因为上面创建表指定这几个字段不能为空
#在session中添加内容
session.add(u)
session.flush() #保存数据
session.commit() #数据库事务的提交,sisson自动过期而不需要关闭

#=========================================
#query() 简单的理解就是select() 的支持 ORM 的替代方法,可以接受任意组合的 class/column 表达式
query = session.query(IPMI)
print list(query) #列出所有user
print query.get(1) #根据主键显示
