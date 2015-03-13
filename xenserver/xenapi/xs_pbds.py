#!/usr/bin/env python
import sys
import XenAPI

session = XenAPI.xapi_local()

try:
    session.login_with_password('', '')
    xenapi = session.xenapi
    records = xenapi.PBDs.get_all_records()
    print records
except:
    sys.exit()

session.xenapi.session.logout() 
