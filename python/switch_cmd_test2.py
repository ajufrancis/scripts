#!/usr/bin/env python
import sys,pexpect
# query file for all route servers and put into a list
routerFile = open('route-servers', 'r')
routeServers = [i for i in routerFile] #look up list comprehension is not clear
# query file for all commands and put into a list
commandFile = open('commands.txt', 'r')
commands = [i for i in commandFile]

fout = file('mylog.txt','w')
# Starts the loop
for router in routeServers:
#    child = pexpect.spawn ('ssh', [router.strip()]) #option needs to be a list
    child = pexpect.spawn('ssh admin@192.168.9.9')
    #child = pexpect.spawn('ssh %s@%s' % (user,ip))

    child.logfile_send = sys.stderr #display progress on screen
    child.logfile_read = fout

    child.expect ('method:')
    child.sendline('Sw04@9.9$')
    for command in commands:
        child.expect(['sw04-ipmi#', 'route-views']) #different options on prompt
        child.sendline(command)
        child.expect(['sw04-ipmi#', 'route-views'])
        child.sendline(command)
