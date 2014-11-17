#!/usr/bin/env python
from fabric.state import env, connections
from fabric.tasks import execute
from fabric.api import *

# fab -f fab-switch.py -R switch -x exclude_host myapp:arg
# fab -f fab-switch.py -H host1,host2 task1:arg task2
env.user = 'admin'
env.output_prefix = False
#https://github.com/fabric/fabric/issues/163
#http://docs.fabfile.org/en/latest/usage/env.html#env-vars
# Example:
#env.output.prefix = "[${hostname} - ${time}] ${cmd_sig}"
#env.output.timeformat = "H:M"
#env.output.cmd_sig = "**"

env.roledefs = {
    'fw_hillstone': ['internet-fw01'],
    'fw_huawei': ['internet-fw02'],
    'r_cisco': ['internet-router01'],
    'vpn_topsec': ['internet-vpn01'],
    'stor_stor02': ['stor02c1', 'stor02c2'],
    'stor_stor03': ['stor03c1', 'stor03c2'],
    'sw_internet': ['internet-sw01'],
    'sw_h3c': ['internet-sw01'],
    'sg_nsfocus': ['access-gateway'],
    'stor_sw': ['storage-sw01', 'storage-sw02'],
    'access_sw': ['access-sw01', 'access-sw02'],
    'core_sw': 'core-sw01'
}

env.hosts = [
        'admin@storage-sw01',
        'admin@storage-sw02',
]

# for env.password,data must be in below format
env.passwords = {
    'admin@storage-sw01:22': 'Tianren.254~s83',
    'admin@storage-sw02:22': 'Tianren.254~s84',
}

#fab -P -z 5 heavy_task
#@parallel(pool_size=5)
#snimpy

def set_hosts(lookup_param):
    # Update env.hosts instead of calling execute()
    env.hosts = external_datastore.query(lookup_param)

@hosts('storage-sw01')
@serial
def sh_int(int=''):
    run('show interface %s | grep -B3 Number' % int)

@roles('stor_sw')
#task groups
#@task(alias='show_system')
#def exec_remote_cmd(cmd):
#    with hide('output','running','warnings'), settings(warn_only=True):
#        return run(cmd)

def sh_sys():
    with settings(hide('running','warnings'), warn_only=True):
        run('show system')
#    import sys
#    cmds = ['show system']
#    for cmd in cmds:
#        result = exec_remote_cmd(cmd)
#        if result.succeeded:
#            sys.stdout.write('\n* Command succeeded: '+cmd+'\n')
#            sys.stdout.write(result+"\n")
#        else:
#            sys.stdout.write('\n* Command failed: '+cmd+'\n')
#            sys.stdout.write(result+"\n")

def put_file():
    with cd('/tmp'):
        put('id_rsa.pub.master', 'id_rsa.pub.master')
        run('cat id_rsa.pub.master >> /root/.ssh/authorized_keys')

def run_task(name, args):
    execute(name, args)

    for key in connections.keys():
        connections[key].close()
        del connections[key]
