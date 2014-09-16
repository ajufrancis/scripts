#!/bin/bash

get_domid() {
  xe vm-list --minimal vm-list name-label=$vm_name params=dom-id
}

get_vncport() {
  xenstore-ls /local/domain/$dom_id/console/vnc-port
}

make_novnc_conf() {
  echo "$vm_name  $ip:$port" > $vm_name.novnc
}
