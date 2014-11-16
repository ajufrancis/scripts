#!/usr/bin/env python
#https://dmsimard.com/2013/11/29/capture-output-from-parallel-execution-with-fabric/
from fabric.api import *

class ParallelCommands():
    def __init__(self, **args):
        self.hosts = args['hosts']
        self.command = args['command']

    @parallel(pool_size=10) # Run on as many as 10 hosts at once
    def parallel_exec(self):
        return run(self.command)

    def capture(self):
        with settings(hide('running', 'commands', 'stdout', 'stderr')):
            stdout = execute(self.parallel_exec, hosts=self.hosts)
        return stdout

"""
The output of each server is inside a dictionary:
{ 'root@server1': 'output', 'root@server2': 'output' }
"""

env.user = 'admin'
hosts = ['storage-sw02']
env.passwords = {
    'admin@storage-sw01:22': 'Tianren.254~s83',
    'admin@storage-sw02:22': 'Tianren.254~s84',
}
#command = 'show system'
command = 'show interfaces | grep -B3 Number'

instance = ParallelCommands(hosts=hosts, command=command)
output = instance.capture()

lines = output['storage-sw02'].split('\n')
state = {}
for i, line in enumerate(lines):
    if line.startswith('Chassis'):
        port = line.split(' ')[2]
        count = lines[i+3].split(':')[-1].strip(',\r').strip(' ')
        lastchanged = lines[i+2].split(' ')[-1]
        port = port.replace('/', '_')
        state[port] = count

import pprint
pp = pprint.PrettyPrinter()
pp.pprint(state)
