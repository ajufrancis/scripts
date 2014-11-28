#!/usr/bin/python
# -*- coding: utf-8 -*- 
import pexpect, sys, os, re, datetime

timestamp = "\n######" + datetime.datetime.now().strftime("%Y-%m-%d-%H:%M") + "######\n"

host = 'internet-fw01'
user = 'hillstone'
passwd = 'Tianren@FW1689.7'
cmd = 'show dnat'
#cmd = 'show admin host'
ssh = pexpect.spawn('ssh %s@%s' % (user, host)) 
#ssh.logfile=sys.stdout

ssh.expect('.*d:.*')
ssh.sendline(passwd)

ssh.expect('.*#.*')
ssh.sendline('terminal length 0')

ssh.expect('.*# ')
ssh.sendline(cmd)

ssh.expect('.*# ')
output = ssh.after.splitlines()

ssh.sendline('\r')
ssh.expect('.*# ')
ssh.sendline('exit')
ssh.close

    
def show_cmd(output):
    for line in output[4:-2]:
      line = line.strip(' ')
      line = re.sub('\s+', ' ', line)
      line = re.sub('=+', '', line)
      print line

show_cmd(output)
