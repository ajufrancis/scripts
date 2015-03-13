#!/usr/bin/env python
import sys
import pprinter
import xapi

s = xapi.Session()
s.login()
print s.this_host
s.logout()
