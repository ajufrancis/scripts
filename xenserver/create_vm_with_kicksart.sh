#!/bin/bash
#https://github.com/mcsrainbow/shell-scripts/blob/master/scripts/xcp_ksinstvm/ksinstvm.sh

pxe_server='pxe.hdtr.com'

vm_name='centos-6.3-x86_64-minmal'
cpu_cores=2
mem_size=2G
disk_size=10G
inst_os='centos6u3-64-minimal.ks'
ksfile='http://{pxe_server}/pxe/ks/linux/{$inst_os}.ks'
repo_url='http://10.24.4.4/os/centos6u3-64'
ks_args="ip=10.24.64.251 netmask=255.255.255.128 gateway=10.24.64.254 ns=10.24.4.85 noipv6 ks=${ksfile} ksdevice=eth0"
 
echo "Creating an empty vm:${vm_name}..."
hostname=$(hostname -s)
sr_uuid=$(xe sr-list | grep -A 2 -B 1 "Local storage" | grep -B 3 -w "${hostname}" | grep uuid | awk -F ": " '{print $2}')
vm_uuid=$(xe vm-install new-name-label=${vm_name} sr-uuid=${sr_uuid} template=Other\ install\ media)
 
echo "Setting up the bootloader,cpu,memory..."
xe vm-param-set VCPUs-max=${cpu_cores} uuid=${vm_uuid}
xe vm-param-set VCPUs-at-startup=${cpu_cores} uuid=${vm_uuid}
xe vm-memory-limits-set uuid=${vm_uuid} dynamic-min=${mem_size}iB dynamic-max=${mem_size}iB static-min=${mem_size}iB static-max=${mem_size}iB
xe vm-param-set HVM-boot-policy="" uuid=${vm_uuid}
xe vm-param-set PV-bootloader="eliloader" uuid=${vm_uuid}
 
echo "Setting up the kickstart..."
xe vm-param-set other-config:install-repository="${repo_url}" uuid=${vm_uuid}
xe vm-param-set PV-args="${ks_args}" uuid=${vm_uuid}
 
echo "Setting up the disk..."
xe vm-disk-add uuid=${vm_uuid} sr-uuid=${sr_uuid} device=0 disk-size=${disk_size}iB
vbd_uuid=$(xe vbd-list vm-uuid=${vm_uuid} userdevice=0 params=uuid --minimal)
xe vbd-param-set bootable=true uuid=${vbd_uuid}
 
echo "Setting up the network..."
network_uuid=$(xe network-list bridge=xenbr0 --minimal)
xe vif-create vm-uuid=${vm_uuid} network-uuid=${network_uuid} mac=random device=0
 
echo "Starting the vm:${vm_name}" 
xe vm-start vm=${vm_name}
