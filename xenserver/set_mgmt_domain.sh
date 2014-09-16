#!/bin/bash

#usage: set_mgmt_domain private hdtr.com
set_mgmt_domain() {
  mgmt_network_label=$1
  domain=$2
  mgmt_pif_list=$(xe pif-list network-name-label=$mgmt_network_label  --minimal | tr ',' '\n')

  for pif in $mgmt_pif_list
  do
    xe pif-param-set uuid=$pif other-config:domain=$domain
  done
}

current_host_id() {
  hostname=`hostname`
  xe host-list --minimal hostname=$hostname
}

# usage: set_live_hostname new_hostname

set_live_hostname() {
    current_hostid=$(current_host_id)
    old_hostname=`hostname`
    new_hostname=$1
    xe host-set-hostname-live host-name=$old_hostname host-uuid=$current_hostid host-name=$new_hostname
    xe host-param-set name-label=$new_hostname uuid=$current_hostid
}

# usage: set_resolv_conf domain_name name_server_ip
set_resolv_conf() {
  cp /etc/resolv.conf /etc/resolv.conf.old
  echo "domain $1" >> /etc/resolv.conf
  echo "search $1" >> /etc/resolv.conf
  echo "nameserver $2" >> /etc/resolv.conf
}
