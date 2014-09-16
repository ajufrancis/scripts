#!/bin/sh
#auto exec command

CMD="$*"
for i in `awk '{print $1}' passwd.txt`
do
    j=`awk -v I="$i" '{if(I==$1)print $2}' passwd.txt`
    expect ./hslogin.exp  $i  $j  "$CMD"
done
