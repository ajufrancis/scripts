#!/bin/bash
IP='192.168.9.6'
USER='admin'
PASSWORD='Tianren.254~s96'
CD='config'
LCD='/srv/scripts/cloudstack/nat'

test -d $LCD || mkdir $LCD

ftp -n <<!
open $IP
user $USER $PASSWORD
prompt
cd $CD
cd $CD
lcd $LCD
mget *
close
bye
!

