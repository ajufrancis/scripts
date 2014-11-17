#!/usr/bin/python
import pexpect
from fabric.colors import *

def ssh_cmd(ip, user, passwd, cmd):
	ssh = pexpect.spawn('ssh %s@%s "%s"' % (user, ip, cmd))
	r = ''
	try:
		i = ssh.expect(['password: ', 'continue connecting (yes/no)?'],timeout=60)
		if i == 0 :
			ssh.sendline(passwd)
		elif i == 1:
			ssh.sendline('yes')
	except pexpect.EOF:
			ssh.close()
	else:
		r = ssh.read()
		ssh.expect(pexpect.EOF)
		return r
		ssh.close()

#192.168.11.8:root:gdcloud.com
#192.168.11.11:root:t1an*8ren168111
#192.168.11.2:root:t1an*8renm11
#192.168.11.3:root:t1an*8renm2
#192.168.11.4:root:t1an*8rendb1
#192.168.11.5:root:t1an*8rendb
#192.168.11.7:root:gdcloud.com
#192.168.11.10:root:gdcloud.com
#192.168.11.12:root:Tianren.312~m11
#192.168.11.13:root:Tianren.313~m2
#192.168.11.14:root:Tianren.481~m
#192.168.11.15:root:Tianren.481~m
#192.168.11.16:root:Tianren.481~m
#192.168.11.17:root:Tianren.481~m
#192.168.11.18:root:Tianren.481~m
#192.168.11.20:root:Tianren.481~m
#192.168.11.25:root:Tianren.112~m
#192.168.11.26:root:Tianren.112~m
#192.168.12.30:root:Bind@in.485
#192.168.12.31:root:Bind@in.485
#192.168.13.12:root:Tianren.131~m

hosts = '''
192.168.13.13:root:Tianren.131~m
192.168.13.14:root:Tianren.131~m
192.168.13.15:root:Tianren.131~m
192.168.14.12:root:Tianren.141~m
192.168.14.13:root:Tianren.141~m
192.168.14.14:root:Tianren.141~m
192.168.14.15:root:Tianren.141~m
192.168.14.21:root:Tianren.142~m
192.168.14.22:root:Tianren.142~m
192.168.14.23:root:Tianren.142~m
192.168.14.221:root:Tianren.143~m
192.168.14.222:root:Tianren.143~m
192.168.14.223:root:Tianren.143~m
192.168.14.224:root:Tianren.143~m
192.168.14.225:root:Tianren.143~m
192.168.14.231:root:Tianren.144~m
192.168.14.232:root:Tianren.144~m
192.168.14.233:root:Tianren.144~m
192.168.14.234:root:Tianren.144~m
192.168.14.235:root:Tianren.144~m
192.168.14.236:root:Tianren.144~m
'''

inst_cmk = '''
rpm -Uvh http://192.168.11.9/tools/nagios/cmk/agent/check_mk-agent-1.2.3i6-1.noarch.rpm
'''

for host in hosts.split("\n"):
	if host:
		ip, user, passwd = host.split(":")
#		for cmd in cmds.split(","):
		print blue("-- %s run:%s --" % (ip, inst_cmk))
		print ssh_cmd(ip, user, passwd, inst_cmk)
