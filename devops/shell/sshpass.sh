#!/bin/bash

PWDFILE='pwd.txt'

cmd="hostname"

while read line
do
   ip=`echo $line | awk -F ' ' '{print $1}'`
   secret=`echo $line | awk -F ' ' '{print $2}'`
   echo $ip:
   echo "----------"
   #sshpass -p "$secret" ssh $ip $cmd
   sshpass -p "$secret" ssh $ip $cmd
done < pwd.txt
