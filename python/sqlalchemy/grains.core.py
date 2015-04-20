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
table_grains_core = Table(
    'tf_grains', metadata,
    Column('uuid', Integer, primary_key=True, nullable=False, default=0),
    Column('minion_id', Unicode(255), unique=True),
    Column('os', Unicode(255), unique=False),
    Column('created', DateTime, default=datetime.now)
)

#在数据库中生成表
metadata.create_all(engine)
#创建一个映射类
class grains_core(object): pass
#把表映射到类
mapper(grains_core, table_grains_core)

#sessionmaker() 函数是最常使用的创建最顶层可用于整个应用 Session 的方法,Session 管理着所有与数据库之间的会话
Session = sessionmaker()
#将创建的数据库连接关联到这个session
Session.configure(bind=engine)
#创建了一个自定义了的 Session类
session = Session()

def get_grains_core():
    import salt.client

    local = salt.client.LocalClient()
    ret = local.cmd('os:XenServer', 'grains.item', ['os'], expr_form='grain')
    return ret

u = grains_core()
ret = get_grains_core()

for output in ret.items():
    id = output[0]  
    os = None
    try:
        os = output[1]['os']
    except:
        continue
    try:
       u.minion_id = id
       u.os = os
       session.add(u)
       session.flush()
       session.commit()
    except:
       continue
