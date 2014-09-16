#!/usr/bin/python
# coding=UTF-8
from ad import Client, Creds, activate
#from ad import Client, Creds, activate

domain = 'hdtr.com'
user = 'administrator'
password = 'gdcloud.com'
server='192.168.12.2'

creds = Creds(domain)
creds.acquire(user, password, server)
activate(creds)

client = ad.Client(domain)
users = client.search('(objectClass=user)')
for dn,attrs in users:
    name = attrs['sAMAccountName'][0]
    print '-> %s' % name
