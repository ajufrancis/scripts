#!/bin/bash
# Author: zh1103@126.com
# README:
# find xenserver' ubuntu vms with xs-tools installed ok,and save VM's PV settings to file
####### WARNING !!! ######
# when VM crashed, it may be restart on a different host from the old which it run, and the
# VM's UUID should be check if it is updated,if so, use the new UUID before runng PV setting commands.
####### WARNING !!! ######
# todo: add cronly task to update
get_vm_uuid() {
  xe vm-list --minimal is-control-domain=false --minimal name-label=$1
}

get_vm_name() {
  xe vm-list --minimal is-control-domain=false --minimal params=name-label uuid=$1
}
get_pv_bootloader_args() {
    UUID=$(get_vm_uuid $1)
    xe vm-list --minimal is-control-domain=false params=PV-bootloader-args uuid=$UUID
}

get_pv_args() {
    UUID=$(get_vm_uuid $1)
    xe vm-list --minimal is-control-domain=false params=PV-args uuid=$UUID
}

get_bootdisk_uuid() {
    UUID=$(get_vm_uuid $1)
    xe vm-disk-list uuid=$UUID | grep -A1 VBD | tail -n 1 | cut -f2 -d: | sed "s/ *//g"
}

get_os_version() {
    if is_xs_tools_installed $1;then
        UUID=$(get_vm_uuid $1)
        xe vm-param-get  uuid=$UUID param-name=os-version  --minimal is-control-domain=false
    fi
}

get_os_name() {
    if is_xs_tools_installed $1;then
        UUID=$(get_vm_uuid $1)
        xe vm-param-get  uuid=$UUID param-name=os-version  --minimal is-control-domain=false | awk -F ';' '{ print $1 }'
    fi
}

get_os_uname() {
    if is_xs_tools_installed $1;then
        UUID=$(get_vm_uuid $1)
        xe vm-param-get  uuid=$UUID param-name=os-version  --minimal is-control-domain=false | awk -F ';' '{ print $1 }'
    fi
}

get_os_distro() {
    if is_xs_tools_installed $1;then
        UUID=$(get_vm_uuid $1)
        xe vm-param-get  uuid=$UUID param-name=os-version  --minimal is-control-domain=false | sed  -n -e 's/^.*distro: //'  -e 's/;.*$//p'
    fi
}

is_xs_tools_installed() {
    UUID=$(get_vm_uuid $1)
    state=$(xe vm-list params=PV-drivers-up-to-date --minimal is-control-domain=false uuid=$UUID)
    case $state in
    'true' )
         return 0
    ;;
    'false' )
         return 0
    ;;
    '<not in database>' )
         return 1
    ;;
    esac
}

is_xs_host() {
  if [ -f /etc/xensource-inventory ];then
    return 0
  else
    return 1
  fi
}


save_ubuntu_pv_settings(){
   VM_NAMES=$(xe vm-list params=name-label --minimal is-control-domain=false | tr ',' '\n') 
   echo > .ubuntu_PV_settings.log
   for VM in $VM_NAMES
   do
     if echo $VM | egrep -v -q 'v-|r-';then
         OS_DISTRO=$(get_os_distro $VM)

         if [ X$OS_DISTRO == Xubuntu ];then
             UUID=$(get_vm_uuid $VM)
             PV_BOOTLOADER_ARGS=$(get_pv_bootloader_args $VM)
             PV_ARGS=$(get_pv_args $VM)
             VBD=$(get_bootdisk_uuid $VM)
             OS_VERSION=$(get_os_version $VM)

             cat << EOT >> .ubuntu_PV_settings.log
##########################
# $VM
# $OS_VERSION
##########################
xe vm-param-set HVM-boot-policy= uuid=$UUID"
xe vm-param-set PV-bootloader=pygrub uuid=$UUID"
xe vm-param-set PV-bootloader-args='$PV_BOOTLOADER_ARGS uuid=$UUID'
xe vm-param-set PV-args='$PV_ARGS' uuid=$UUID"
xe vbd-param-set bootable=true uuid=$VBD"
EOT
         fi
     fi
   done
}

is_xs_host || $(echo "must to ruunig on XenServer host" && exit 1)
save_ubuntu_pv_settings
