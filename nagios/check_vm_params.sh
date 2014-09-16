#!/bin/bash

while read key value
do
  key = $value
  cur_value=`xe vm-list --minimal params=$key --minimal`
  if [ $cur_value = $value ];then
    echo "$vm_name: all params set as expected"
    exit 0
  else
    echo "$vm_name current $key is: $cur_value(mismatch)"
    exit 1
  fi
done < ~/.ubuntu_pv_params/$vm_name.log
