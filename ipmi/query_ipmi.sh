#!/bin/bash
IPMI_IP=`ipmitool lan print 1 | grep 'IP Address' | tail -1 | cut -d ':' -f2`
echo $IPMI_IP

