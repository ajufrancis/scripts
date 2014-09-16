#!/bin/bash
vm_uuid_list=$(xe vm-list --minimal | tr ',' '\n')

for vm_uuid in `echo $vm_uuid_list`
do
    vif_uuid_list=$(xe vif-list vm-uuid=$vm_uuid  --minimal | grep -v ,)
    for vif_uuid in `echo $vif_uuid_list`
    do
        xe vif-param-get param-name=network-name-label uuid=$vif_uuid 
    done
done
