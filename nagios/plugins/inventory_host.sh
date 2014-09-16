#!/bin/bash

ssh_port=22
rdp_port=3389

function scan_host()
{
	HOST=$1
	if `tcping -t 1 $HOST $ssh_port 2>&1 > /dev/null`
	then
		echo $HOST:$ssh_port:LINUX
	elif `tcping -t 1 $HOST $rdp_port 2>&1 > /dev/null`
	then
		echo $HOST:$rdp_port:WINDOWS
	elif `ping -w 1 $HOST 2>&1 > /dev/null`
	then
		echo $HOST::UNKNOWN
	fi
}
for i in `seq 1 250`
do
	scan_host "10.24.56.$i"
done
