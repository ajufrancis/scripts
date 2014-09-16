#!/bin/bash
# usage: $0 vm_name

get_dom_id() {
  if [ -f /etc/xensource-inventory ];then
    vm_name=$1
    dom_id=$(xl list-vm | sed -n 's/\s\+/ /gp' | grep $vm_name | awk '{ print $2}')
    echo $dom_id
  else
    echo "$0 only run on XenServer Hypervisor !" && exit 1
  fi
}

destroy_domain() {
  dom_id=$1
  /opt/xensource/debug/xenops destroy_domain -domid $dom_id
}

dom_id=$(get_dom_id $1)
if [ -z $dom_id ];then
  echo "vm not found !" && exit 1
else
   destroy_domain $dom_id
fi
