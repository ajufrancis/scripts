#!/usr/bin/python
# -*- coding: utf-8 -*- 
import pexpect, sys, os, re, datetime

timestamp = "\n######" + datetime.datetime.now().strftime("%Y-%m-%d-%H:%M") + "######\n"

def run_cmd(host, user, password, cmd):

  ssh = pexpect.spawn('ssh %s@%s' % (user, host)) 
  #ssh.logfile=sys.stdout
  ssh.expect('.*d:.*')
  ssh.sendline(password)
  ssh.expect('.*#.*')
  ssh.sendline('terminal length 0')
  ssh.expect('.*# ')
  ssh.sendline(cmd)
  ssh.expect('.*# ')
  dnatrule_list = ssh.after.splitlines()
  ssh.sendline('\r')
  ssh.expect('.*# ')
  ssh.sendline('exit')
  ssh.close
  return dnatrule_list


rules = run_cmd('192.168.9.6', 'pexpect', 'P@$w0rD01!', 'show config | inc dnat')
