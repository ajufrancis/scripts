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

env.user = 'hillstone'
hosts = ['internet-fw01']
env.passwords = {
    'hillstone@internet-fw01:22': 'Tianren@FW1689.7'
}
command = 'show dnat'

instance = ParallelCommands(hosts=hosts, command=command)
output = instance.capture()

lines = output['internet-fw01'].split('\n')
rules = []
for i, dnat in enumerate(lines):
    print i, dnat
   
import pprint
#pp = pprint.PrettyPrinter()
#pp.pprint(state)
