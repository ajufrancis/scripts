#!/usr/bin/python
import pexpect

child=pexpect.spawn('ssh admin@192.168.9.10')
child.expect('.*:')
child.sendline('Tianren.254~s910')
child.expect('.*#')
child.sendline('show ntp server status')
child.expect('.*#')
print "child.before: " + child.before
print "child.after: " + child.after
child.sendline('exit')
child.close                    
