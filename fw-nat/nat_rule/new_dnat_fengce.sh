#!/bin/bash

while read line
do
  ip=`echo $line | cut -d ' ' -f3`
  echo $i
done< fengce-vm.list
