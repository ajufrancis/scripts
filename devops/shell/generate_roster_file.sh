#!/bin/bash

if [ -e ./xs.roster ];then
  pwdfile='./xs.roster'
else
  echo "./xs.roster not found !"
  exit 1
fi

i=1
while read line
do
  ip=`echo $line | awk -F ':' '{print $1}'`
  secret=`echo $line | awk -F ':' '{print $3}'`
  echo "xsc$i"
  echo "  host: $ip"
  echo "  user: root"
  echo "  passwd: $secret"
  let i=$i+1
done < $pwdfile
