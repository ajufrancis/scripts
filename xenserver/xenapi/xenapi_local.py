#!/usr/bin/env python
import sys
import XenAPI

session = XenAPI.xapi_local()
try:
    session.login_with_password('', '')
    xenapi = session.xenapi
    records = xenapi.session.this_host()
    print records
except:
    session.xenapi.session.logout()
    sys.exit()
