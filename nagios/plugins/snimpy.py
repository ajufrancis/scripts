#!/usr/bin/env snimpy
load('/usr/share/snmp/mibs/SNMPv2-MIB.txt')
m = M("192.168.8.3","snmp-com-ro",2)
print m.sysDescr
