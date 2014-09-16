#!/bin/sh
#auto exec command

for i in `awk '{print $1}' xs_host.txt`
do
    j=`awk -v I="$i" '{if(I==$1)print $2}' xs_host.txt`
    k=`awk -v I="$i" '{if(I==$1)print $3}' xs_host.txt`
    expect ./set_ipmi_password.exp  $i  $j  $k
done
