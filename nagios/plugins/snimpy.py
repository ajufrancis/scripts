#!/usr/bin/env snimpy
load('/usr/share/snmp/mibs/NETWORK-APPLIANCE-MIB.mib')
m = M("192.168.11.31","snmp4stor02",2)
print 'FAN state:',
print m.envFailedFanCount
print 'Temperature:',
print m.envOverTemperature
print 'PowerSupply:',
print m.envFailedPowerSupplyCount
print 'CPU busytime percent:',
print m.cpuBusyTimePerCent
