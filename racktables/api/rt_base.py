#!/usr/bin/python
#sms_5c.py
import sys, os
import StringIO
import json
import pycurl, urllib

def api(method, params={}):
    username = 'zhanghu'
    password = 'zhanghu'
    host = '10.24.4.48'
    url = 'http://%s:%s@%s/racktables/api.php' % (username, password, host)
    params.update({'method': method})
    if args:
        for item in args.items():
            params.update(item)

    post_data = urllib.urlencode(params)

    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.CONNECTTIMEOUT, 60)
    c.setopt(c.POSTFIELDS, post_data)
    
    data = None
    try:
        b = StringIO.StringIO()
        c.setopt(c.WRITEFUNCTION, b.write)
        c.perform()
        data=b.getvalue()
        b.close()
        c.close()
    
    except pycurl.error, error:
        errno, errstr = error
        print 'An error occurred: ', errstr

    dict = json.loads(data)
    return dict['response']

def get_depot(params):
    depot = get_data(method='get_depot')
    return depot

def get_rackspace(params):
    rackspace = get_data(method='get_rackspace')
    return rackspace

def get_tagtree():
    tagtree = get_data(method='get_tagtree')
    return tagtree
    
def get_taglist(params={}):
    taglist = get_data(method='get_taglist', params) 
    return taglist

def get_attributes():
    attributes = get_data(method='get_attributes')
    return attributes

def get_dictionary():
    dictionary = get_data(method='get_dictionary')
    return dictionary

def get_ipv4network():
    ipv4network = get_data(method='get_ipv4network')
    return ipv4network

def get_vlan_domains():
    vlan_domains = get_data(method='get_vlan_domains')
    return vlan_domains
