#!/bin/bash
wget -O ChinaTelcom.txt http://files.liubaishui.com/ChinaTelcom.txt
wget -O UNICOM_CNC.txt http://files.liubaishui.com/UNICOM_CNC.txt
wget -O CTT.txt http://files.liubaishui.com/CTT.txt
wget -O CMCC.txt http://files.liubaishui.com/CMCC.txt

echo "
# NOTICE: Keep the following comment lines intact!!!
# A line leading by '#' is a comment line.
# Mapping relation: [abbr.] --- ISP
# abbr. should be 'A~Z', ISP name length 1~31.
# ISP name is composed of alphabet and '-', '*', '&'.
A --- ChinaTelcom
# ChinaTelcom
" > ChinaTelcom.DAT
sed -n '/^[1-9]/p' ChinaTelcom.txt >> ChinaTelcom.DAT
sed -i '/^[1-9]/s/;//' ChinaTelcom.DAT
sed -i '/^[1-9]/s/^/A:/' ChinaTelcom.DAT
