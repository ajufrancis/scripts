#!/usr/bin/python
# encoding=utf-8
# Filename: pexpect_test.py
import pexpect

def sshCmd(ip, passwd, cmd):
    ret = -1
    ssh = pexpect.spawn('ssh hillstone@%s "%s"' % (ip, cmd))
    try:
        i = ssh.expect(['password:', 'continue connecting(yes/no)?'], timeout=5)
        if i == 0:
            ssh.sendline(passwd)
        elif i == 1:
            ssh.sendline('yes')
            ssh.expect('password:')
            ssh.sendline(passwd)
        ssh.sendline(cmd)
        r = ssh.read()
        print r
        ret = 0
    except pexpect.EOF:
        print "EOF"
        ret = -1
    except pexpect.TIMEOUT:
        print "TIMEOUT"
        ret = -2
    finally:
        ssh.close()
    return ret
 
host = 'internet-fw01'
passwd = 'Tianren@FW1689.7'
cmd = 'show admin host'
sshCmd(host, passwd, cmd)
