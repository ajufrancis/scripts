#!/bin/bash
#TODO
# grouping: CNC/CTC/LAN/WAN addresses
#
wget ftp://backup:backup@192.168.12.1/hillstone-SG6000.2014-01-16-16-00
INPUT="hillstone-SG6000.2014-01-16-16-00"
FW_DNAT="fw_dnatrule.txt"
FW_PNAT="fw_pnatrule.txt"
FW_SERVICES="fw_services.txt"
FW_SERVGROUP="fw_servgroup.txt"

RT_DNAT="rt_dnatrule.txt"
RT_PNAT="rt_pnatrule.txt"

# get DNAT rules
grep dnatrule $INPUT > tmp.txt
grep -v port tmp.txt > $FW_DNAT
# format service Any to blank
sed -i 's/service\ "Any"\ //' $FW_DNAT
# format " to blank
sed -i 's/"//g' $FW_DNAT
# sort ip
awk '{print $9,$7}' $FW_DNAT | sort -n -t . -k 1,1 -k 2,2 -k 3,3 -k 4,4 > $RT_DNAT
#delete lines has char
grep -q [a-zA-Z] $RT_DNAT && echo ERROR
sed -i '/[a-zA-Z]/d' $RT_DNAT

# get PNAT rules
grep dnatrule $INPUT > tmp.txt
grep port tmp.txt > $FW_PNAT
awk '{print $11,$13,$7,$9}' $FW_PNAT | sort -n -t . -k 1,1 -k 2,2 -k 3,3 -k 4,4 > $RT_PNAT
sed -i 's/"//g' $RT_PNAT

# get service name
awk '/service /,/exit/' $INPUT > $FW_SERVICES
#
rm -f tmp.txt
