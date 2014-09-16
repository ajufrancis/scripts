#!/usr/bin/env python
#usage: fab -R 'ops' -f firstboot.py cmd

from fabric.api import env, hosts, roles, run

# role['name']
# role['value']
# role['user']
# role['password']
# env.password = role['password']
env.user='root'
#env.password='Tianren.481~m'
#env.password='Tianren.131~m'
#env.password='Tianren.141~m'
#env.password='gdcloud.com'

env.roledefs = {
 'ops':[
  '192.168.12.1',
  '192.168.12.9',
  '192.168.31.245',
 ] 
}


# 'ops':[
#  '192.168.11.6',
#  '192.168.11.7',
#  '192.168.11.8',
#  '192.168.11.9',
#  '192.168.11.10',
#  '192.168.12.1',
#  '192.168.12.6',
#  '192.168.12.7',
#  '192.168.12.8',
#  '192.168.12.9',
#  '192.168.31.245',
#]

#'z3p1c1':['192.168.14.12','192.168.14.13','192.168.14.14','192.168.14.15']
#  'prod':['192.168.11.14','192.168.11.15','192.168.11.18','192.168.11.16','192.168.11.20']
#  'gdupc':['192.168.13.12','192.168.13.13','192.168.13.14','192.168.13.15']
#  'prod':['192.168.11.14','192.168.11.15','192.168.11.18','192.168.11.16','192.168.11.20']
#  'z3p1c1':['192.168.14.12','192.168.14.13','192.168.14.14','192.168.14.15']
#'z3p1c1':['192.168.14.12','192.168.14.13','192.168.14.14','192.168.14.15']

#  'z3p1c2':['192.168.14.21','192.168.14.22','192.168.14.23']
#
#'z3p1c3':['192.168.14.221 z3p1c3 192.168.14.222 z3p1c3 192.168.14.223 z3p1c3 192.168.14.224 z3p1c3 192.168.14.225
#'khjtz2p1c2':['192.168.11.25 khjtz2p1c2 192.168.11.26 khjtz2p1c2 192.168.11.27
#'z3p1c4':['192.168.14.231 z3p1c4 192.168.14.232 z3p1c4 192.168.14.233 z3p1c4 192.168.14.234 z3p1c4 192.168.14.235 z3p1c4 192.168.14.236
#'z2p201c1':['192.168.201.1

#@roles('z3p1c1')
def cmk_version():
  run('rpm -qa | grep check_mk-agent')
def inst_cmk():
  run('wget -P /tmp http://10.24.4.4/software/nagios/cmk/agent/check_mk-agent-logwatch-1.2.3i7p2-1.noarch.rpm') 
  run('rpm -Uvh /tmp/check_mk-agent-logwatch-1.2.3i7p2-1.noarch.rpm')
def add_plugins():
  run('rm -f /usr/lib/check_mk_agent/plugins/check_xs-tools')
  run('wget -O /usr/lib/check_mk_agent/plugins/check_xs-tools http://10.24.4.84/tools/nagios/plugins/xenserver/check_xs-tools') 
  run('chmod a+x /usr/lib/check_mk_agent/plugins/check_xs-tools')
def repo_info():
  run('ls /etc/yum.repos.d')
def cmk_status():
  run('netstat -nlptua |grep 6556')
def salt_service():
  run('netstat -nlptua | grep salt')
def salt_info():
  run('rpm -qa| grep salt-minion')
def salt_start():
  run('chkconfig salt-minion on')
  run('service salt-minion restart')
def ipt_status():
  run('iptables -L')
  run('chkconfig --list iptables')
def yum_conf():
  run('wget -O /etc/yum.conf http://10.24.4.84/pxe/saltstack/etc/yum.conf')
  run('chmod 644 /etc/yum.conf')
  run('chmod 644 /etc/yum.repos.d/*.repo')
def get_repo():
  run('wget -O /etc/yum.repos.d/epel.repo http://10.24.4.84/pxe/saltstack/etc/yum.repos.d/epel.repo')
  run('wget -O /etc/yum.repos.d/rpmforge.repo http://10.24.4.84/pxe/saltstack/etc/yum.repos.d/rpmforge.repo')
  run('wget -O /etc/yum.repos.d/CentOS-Base.repo http://10.24.4.84/pxe/saltstack/etc/yum.repos.d/CentOS-Base.repo')
  run('chmod 644 /etc/yum.repos.d/*.repo')
def clean_repo():
  run('yum clean all')
  run('yum makecache 1>2')
def inst_salt():
  run('yum -y install salt-minion --nogpgcheck')
def salt_version():
  run('rpm -qa | grep salt')
def salt_conf():
  run('wget -O /etc/salt/minion http://10.24.4.84/pxe/saltstack/etc/salt/minion')
def start_salt():
  run('service salt-minion start')
  run('chkconfig salt-minion on')
#def check_hostname
#def check_resolv
#def check_ipv6
#def check_selinux
#def check_iptables
#def check_packages
#mlocate/wget/curl/perl/php/python
#def check_yum_conf
#def check_yum_repos
#def check_yum_plugins
#def check_sshd_config
#def inst_ocs():
#def remove_ocs():
#def ocs_version():
#def ocs_status():
#
#def os_info():
#def host_info():
#
#def inst_sflow():
#def sflow_status():
#def start_sflow():
#def stop_sflow():
#
#def load_ipmi_mod():
#def inst_ipmitool():
#def ipmi_info():
#
#def inst_xstools():
#def update_xstools():
#def xstools_version():
