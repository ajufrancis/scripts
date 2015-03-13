#!/usr/bin/python
#sms_5c.py
import sys, os
import StringIO
import json
import pycurl, urllib
import pprint

def get_data():
    username = 'zhanghu'
    password = 'zhanghu'
    host = '10.24.4.48'
    url = 'http://%s:%s@%s/racktables/api.php' % (username, password, host)
    params = {
        'method': 'get_depot'
    }
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

    return data

data = get_data()
dict = json.loads(data)
pp = pprint.PrettyPrinter()
pp.pprint(dict)
