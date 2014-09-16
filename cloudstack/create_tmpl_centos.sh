hostname localhost
echo "localhost" > /etc/hostname
password='gdcloud!.2013'
echo "$password" | passwd --stdin root
passwd --expire root

cat << EOF > /etc/sysconfig/network-scripts/ifcfg-eth0
DEVICE=eth0
TYPE=Ethernet
BOOTPROTO=dhcp
ONBOOT=yes
EOF

rm -f /etc/udev/rules.d/70*
rm -f /var/lib/dhclient/*
rm -f /etc/ssh/*key*
cat /dev/null > /var/log/audit/audit.log 2>/dev/null
cat /dev/null > /var/log/wtmp 2>/dev/null
logrotate -f /etc/logrotate.conf 2>/dev/null
rm -f /var/log/*-* /var/log/*.gz 2>/dev/null

history -c
unset HISTFILE
halt -p
