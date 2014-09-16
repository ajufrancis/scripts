#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

from pysnmp.smi import builder

# create MIB builder
mibBuilder = builder.MibBuilder().loadModules('NMPv2-MIB', 'IF-MIB')

# get Managed Object definition by symbol name
node = mibBuilder.importSymbols('SNMPv2-MIB', 'sysDescr')
print 'name:', node.getName()
print 'status:', node.getStatus()
print 'syntax:', repr(node.getSyntax())
