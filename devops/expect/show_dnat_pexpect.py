#!/usr/bin/python
# -*- coding: utf-8 -*- 
import pexpect, sys, os

ssh = pexpect.spawn('ssh %s@%s' % ('hillstone','192.168.9.6')) 
#ssh.logfile=sys.stdout
ssh.expect('.*d:.*')
ssh.sendline('Tianren@FW1689.7')
ssh.expect('.*#.*')
ssh.sendline('terminal length 0')
ssh.expect('.*# ')
ssh.sendline('show dnat | inc 10.24.56')
ssh.expect('.*# ')
print ssh.after
ssh.sendline('\r')
ssh.expect('.*# ')
ssh.sendline('exit')
ssh.close
