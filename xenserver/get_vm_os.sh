get_os_info() {
  xe vm-list name-label=$1 params=os-version PV-driver-up-to-date=true --minimal uuid=`xl list-vm | grep $name | cut -d ' ' -f 1`
}
