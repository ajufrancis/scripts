#!/bin/bash

#########################
# clear firstrun
#########################
if
  which xe-linux-distribution >/dev/null 2>&1
then
  sed -i '/firstrun/d' /etc/rc.local
  exit
else
  mount -t nfs ${nfs_server}:${exports} ${mnt}
  echo y | ${mnt}/xstools/Linux/install.sh
fi

#########################
# global settings
#########################

nfs_server="192.168.11.9"
exports="/var/www/html/exports"
mnt="/mnt"
ntp_server="192.168.11.10"

#########################
# yum settings
#########################
cp ${mnt}/yum/*.repo /etc/yum.repos.d/
yum makecache
yum install wget -y
#########################
# set ntp
#########################
ntpdate -u ${ntp_server} && hwclock -w
sed -i 's/SYNC_HWCLOCK=no/SYNC_HWCLOCK=yes/' /etc/sysconfig/ntpdate
# chkconfig ntpdate on
# service ntpdate start
#########################
# set ssh
#########################
sed -i '/GSSAPIAuthentication/s/yes/no/' /etc/ssh/sshd_config
sed -i '/UseDNS/s/yes/no/' /etc/ssh/sshd_config
service sshd reload
#########################
# set services
#########################
setenforce 0
sed -i '/SELINUX=/s/enforcing/disabled/' /etc/sysconfig/selinux
#########################
# set others
#########################
#cmk
#ocsng
#hsflow
#fabric
#hwinfo

#########################
# vncserver settings 
#########################

if [ -d /proc/xen ]
then
	yum install -y pixman libXfont tigervnc-server xrdp --nogpgcheck

fi

echo 'VNCSERVERS="2:root"' >> /etc/sysconfig/vncservers
chkconfig xrdp on
chkconfig vncserver on
service xrdp start

#echo "set vncpasswd:"
#vncpasswd 
#service vncserver start
#########################
# umount nfs && reboot
#########################

cd / && umount /mnt && reboot
