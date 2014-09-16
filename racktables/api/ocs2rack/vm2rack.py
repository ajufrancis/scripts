#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = '0.2'

import sys
import os
import ConfigParser
import socket

try:
    import MySQLdb
    import MySQLdb.cursors
except:
    print(
        'CS_VM_to_RackTables need python module MySQLdb: {0}'.format(sys.exc_info()[1]))
    sys.exit(1)

try:
    from IPy import IP
except:
    print('CS_VM_to_RackTables need python module IPy: {0}'.format(sys.exc_info()[1]))
    sys.exit(1)

try:
    import CloudStack
except:
    print('CS_VM_to_RackTables need python module CloudStack: {0}'.format(sys.exc_info()[1]))
    sys.exit(1)

objtype_maps = {
    'Server': '4',
    'VM': '1504',
}
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ConfigError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Config(object):

    CONFIG_DEFAULT_ENV_NAME = 'OCS2RACK_CONFIG'

    def __init__(self):
        try:
            self._config_filename = sys.argv[1]
        except:
            self._config_filename = os.environ.get(
                self.CONFIG_DEFAULT_ENV_NAME,
                os.path.join(
                    os.path.dirname(sys.argv[0]),
                    'ocs2rack.conf'))
            pass

        self._config_handler = ConfigParser.RawConfigParser()

        if not self._config_handler.read(self._config_filename):
            raise ConfigError(
                'Configuration file not found: "{0}"'.format(self._config_filename))

    def get_bool(self, section, option):
        return self._config_handler.getboolean(section, option)

    def get_int(self, section, option):
        return self._config_handler.getint(section, option)

    def get(self, section, option):
        return self._config_handler.get(section, option)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class RACK(object):

    ATTR_OEM_SN1 = 1
    ATTR_HW_TYPE = 2
    ATTR_FQDN = 3
    ATTR_SW_TYPE = 4
    ATTR_SW_VERSION = 5
    ATTR_DRAM_MB = 17
    ATTR_CPU_MHZ = 18

    def __init__(self, config):
        self._config = config

        try:
            self._db = MySQLdb.connect(
                host=config.get('rack', 'db_host'),
                db=config.get('rack', 'db_name'),
                user=config.get('rack', 'db_user'),
                passwd=config.get('rack', 'db_pass'),
                use_unicode=True,
                cursorclass=MySQLdb.cursors.DictCursor)
        except:
            print(sys.exc_info()[1])
            sys.exit(1)

        self._db.autocommit(True)
        self._curs = self._db.cursor()

    def check_RackObject(self, asset):
        objtype_id = objtype_maps[asset['obj_type']]
        name = asset['cn_name']
        sql = "SELECT id FROM RackObject WHERE name='{0}' AND objtype_id = {1}".format(asset['cn_name'], objtype_id)
#        print sql
        result = self._curs.execute(sql)
        if self._curs.rowcount:
            return self._curs.fetchone()['id']
        return 0

#    def add_object(self, name, label='', objtype_name, asset_no=None, pb='no', comment=''):
    def add_object(self, asset):
        name = asset['cn_name']
        label = asset['label']
        objtype_id = objtype_maps[asset['obj_type']]
        asset_no = asset['asset_no']
        pb = asset['pb']
        comment = asset['comment']
        time = 
        sql = "INSERT INTO RackObject ( name, label, objtype_id, asset_no, has_problems, comment ) VALUES ('{0}','{1}',{2},'{3}',{4},'{5}')".format(name, label, objtype_id, asset_no, pb, comment)
        self._curs.execute(sql)
        return self._curs.lastrowid

    def check_add_ip_network(self, ip, netmask):
        ipnet = IP(ip).make_net(netmask)
        ip_dec = int(ipnet.strDec())
        ip_prefixlen = ipnet.prefixlen()

        sql_check = '''SELECT 1 FROM {0} WHERE ip = %s AND mask = %s'''
        sql_add = '\n'.join([
            'INSERT INTO {0}',
            '    ( ip, mask, name, comment )',
            'VALUES',
            '''( %s, %s, %s, 'Imported by ocs2rack' )''',
        ])

        if ipnet.version() == 6:
            sql_check = sql_check.format('IPv6Network')
            sql_add = sql_add.format('IPv6Network')
        else:
            sql_check = sql_check.format('IPv4Network')
            sql_add = sql_add.format('IPv4Network')

        self._curs.execute(sql_check, (ip_dec, ip_prefixlen))
        if self._curs.rowcount:
            return 0

        self._curs.execute(
            sql_add, (ip_dec, ip_prefixlen, ipnet.reverseName()))
        return self._curs.rowcount

    def check_ip_allocation(self, asset):
        rack_object_id = self.check_RackObject(asset)
        ip_addr = asset['ip']
        if_name = asset['if_name']
        if_type = asset['if_type']
        ipnet = IP(ip_addr)
        ip_dec = int(ipnet.strDec())

        if ipnet.version() == 6:
            sql_check = "SELECT 1 FROM IPv6Allocation WHERE object_id = {0} AND ip = '{1}' AND name = '{2}' AND type = '{3}'".format(rack_object_id, ip_addr, if_name, if_type)
        else:
            sql_check = "SELECT 1 FROM IPv4Allocation WHERE object_id = {0} AND ip = '{1}' AND name = '{2}' AND type = '{3}'".format(rack_object_id, ip_addr, if_name, if_type)

        self._curs.execute(sql_check)
        if self._curs.rowcount:
            return 0

        return self._curs.rowcount

    def append(self, asset):
        # a CloudStatck VM dict
        #-- Is server already exists in rack ?

        rack_object_id = self.check_RackObject(asset)

        if rack_object_id:
            print "{0}: {1}' already exist ! skip to next vm ...".format(asset['name'], asset['obj_type'])
        else:
        # if not, add vm with comment
            for k in asset.keys():
                asset['comment'] += '{0}: {1}\n'.format(k, asset[k])

            rack_object_id = self.add_object(asset)

            print(
                '\t+New rack_object id #{0}({1}) created'.format(rack_object_id, asset['name']))
    def check_entitylink(self, asset):
        sql_check_entitylink = "SELECT FROM EntityLink WHERE parent_entity_type='object' and child_entity_type='object' and parent_entity_id='{0}' and child_entity_id='{1}' ".format(parent_entity_id,  child_entity_id )
        self._curs.execute(sql_check_entitylink)
        if self._curs.rowcount:
            return self._curs.fetchone()['id']
        return self._curs.rowcount

    def add_entitylink(self, asset):
        try:
            parent_entity_id  = self.check_RackObject(asset['hostname'])
            child_entity_id  = self.check_RackObject(asset['cn_name'])
            sql_add_entitylink = "INSERT INTO EntityLink VALUES ('object', {0}, 'object', {1})".format('object', parent_entity_id, 'object', child_entity_id )
            self._curs.execute(sql_add_entitylink)
            return self._curs.rowcount

        except:
            if not asset.has_key('hostname'):
                print "ENTITYLINK_ADD: Failed, may be"
            else:
                print "Unknown Error !"

    def add_ip(self, asset):
        #-- Check/Add IP to rack object
        try:
            if self.check_ip_allocation(asset):
                print "IP_ALLOCATION_EXIST:{0}:{1} {2}@{3}:{4}".format(rack_object_id, asset['cn_name'], asset['ip'], asset['if_name'], asset['if_type'])
       
            else:
                rack_object_id = self.check_RackObject(asset)
                ip_addr = asset['ip']
                ipnet = IP(ip_addr)
                ip_dec = int(ipnet.strDec())
                if_name = asset['if_name']
                if_type = asset['if_type']

                if ipnet.version() == 6:
                    sql_add = "INSERT IGNORE INTO IPv6Allocation VALUES ({0}, '{1}', '{2}', '{3}')".format(rack_object_id, ip_dec, if_name, if_type)
                else:
                    sql_add = "INSERT IGNORE INTO IPv4Allocation VALUES ({0}, '{1}', '{2}', '{3}')".format(rack_object_id, ip_dec, if_name, if_type)

                self._curs.execute(sql_add)

                print "IP_ALLOCATION_NEW: {0}:{1} {2}@{3}:{4}".format(rack_object_id, asset['cn_name'], asset['ip'], asset['if_name'], asset['if_type'])
                return self._curs.rowcount
        except:
            print "IP_LOST: {1}@{0}".format(asset['cn_name'], asset['obj_type'])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class CloudStackClient(object):

    def __init__(self, config):
        self._config = config

        try:
                api=config.get('cloud', 'api')
                apikey=config.get('cloud', 'apikey')
                secret=config.get('cloud', 'secret')

                self._api = CloudStack.Client(api, apikey, secret)

        except:
            print(sys.exc_info()[1])
            sys.exit(1)

    def list_all_vms(self):
         output = self._api.listVirtualMachines({'listall': 'true'})
         return output
    def list_all_host(self):
         output = self._api.listVirtualMachines({'listall': 'true'})
         return output
    def list_all_vrouter(self):
         output = self._api.listVirtualMachines({'listall': 'true'})
         return output
    def list_all_ssvm(self):
         output = self._api.listVirtualMachines({'listall': 'true'})
         return output
    def list_all_account(self):
         output = self._api.listVirtualMachines({'listall': 'true'})
         return output

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class RackAsset(object):
# provide a dict object

    def __init__(self, asset):
        self.info = object
        self.info['pb'] = 'no'

        if object.has_key('instancename'):
            self.info['obj_type'] = 'VM'
            self.info['model'] = 'Unknown'
            self.info['label'] = object['name']
            self.info['asset_no'] = object['id']
            self.info['comment'] = 'info'

    def info(self):
        print type(self.info)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# if_type = ['shared', 'connected', 'regular', 'virtual', 'router', 'p2p']
#            'hostname',    
#            'natip',    
def Asset(obj):
        asset = obj
        asset['obj_type'] = 'VM'
        asset['cn_name'] = obj['instancename']
        asset['label'] = obj['name']
        asset['asset_no'] = obj['id']
        asset['pb'] = 'no'
        asset['if_name'] = 'publicip'
        asset['if_type'] = 'shared'

        asset['comment'] = ''
        import datetime
        asset['timestamp'] = datetime.now()

        for k in ['created',
            'created',    
            'state',    
            'haenable',    
            'cpunumber',    
            'cpuspeed',    
            'memory',    
            'account',    
            'serviceofferingname',    
            ]:
            asset['comment'] += '{0}: {1}\n'.format(k, obj[k])

        asset['mac'] = obj['nic'][0]['macaddress']

        try:
            if asset['nic'][0]['type'] == 'Shared':
                asset['ip'] = str(obj['nic'][0]['ipaddress'])
                asset['gateway'] = str(obj['nic'][0]['gateway'])
            if asset['nic'][0]['type'] == 'Isolated':
                asset['ip'] = obj['publicip']
        except:
            print "IP lost: {0}: {1}".format(asset['obj_type'], obj['instancename'])

        return asset

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    config = Config()
    rack = RACK(config)

    test = [
{u'domain': u'ROOT', u'domainid': u'9b832394-f254-4f6d-ba67-ed3979ac9fc6', u'haenable': False, u'templatename': u'windows_2008_r2_sp1_x64', u'securitygroup': [], u'zoneid': u'8e19be3a-c953-4dec-aa74-857226de927c', u'cpunumber': 4, u'passwordenabled': False, u'instancename': u'i-21-2294-VM', u'id': u'a929693b-c0bf-4692-a317-d3f3b7aabcd1', u'cpuused': u'0.41%', u'hostname': u'xstest2', u'publicip': u'192.168.31.189', u'state': u'Running', u'guestosid': u'fda2b5fb-62a1-463b-b366-e395c11486d4', u'networkkbswrite': 88882, u'memory': 8096, u'serviceofferingid': u'3cbbfa4e-be8f-4ccb-9a3d-86dda62501f2', u'zonename': u'zone-prod', u'displayname': u'base-win2008', u'nic': [{u'networkid': u'5203d048-6b2d-4afe-a851-22cf5cafb4fc', u'macaddress': u'02:00:6c:69:00:4c', u'type': u'Isolated', u'gateway': u'10.1.1.1', u'traffictype': u'Guest', u'netmask': u'255.255.255.0', u'ipaddress': u'10.1.1.33', u'id': u'2209eed2-b052-4879-9c22-c10a46705737', u'isdefault': True}], u'cpuspeed': 2600, u'templateid': u'5b021312-58cc-4825-869c-a4fc1e52c874', u'account': u'test', u'hostid': u'326377c3-8745-4c4f-93da-9ec125ae41ce', u'name': u'base-win2008', u'networkkbsread': 111973, u'created': u'2014-08-13T15:34:51+0800', u'hypervisor': u'XenServer', u'publicipid': u'ac836830-f108-4d1b-b231-32d6c2acfe36', u'rootdevicetype': u'NetworkFilesystem', u'rootdeviceid': 0, u'serviceofferingname': u'test-z2p201c1-4CPU-8G-secst', u'templatedisplaytext': u'windows_2008_r2_sp1_x64_enterprise_activated'}
]
    hadoop3 = [{u'domain': u'ROOT', u'domainid': u'9b832394-f254-4f6d-ba67-ed3979ac9fc6', u'haenable': False, u'templatename': u'jtcaiwuapp-rehl6.3-64-50G', u'securitygroup': [], u'zoneid': u'8e19be3a-c953-4dec-aa74-857226de927c', u'cpunumber': 4, u'passwordenabled': False, u'instancename': u'i-21-2289-VM', u'id': u'65315b2d-6c22-43b7-9f2f-764b0843e7ce', u'cpuused': u'7.38%', u'hostname': u'xstest1.gdcloud.com', u'state': u'Running', u'guestosid': u'7436a37e-8e1d-4ee4-81b1-5f98e6d7543b', u'networkkbswrite': 26174358, u'memory': 8096, u'serviceofferingid': u'3cbbfa4e-be8f-4ccb-9a3d-86dda62501f2', u'zonename': u'zone-prod', u'displayname': u'hadoop3', u'nic': [{u'networkid': u'8d1489ae-8db9-4d5d-b34e-d9545a885973', u'macaddress': u'02:00:7a:df:00:47', u'type': u'Shared', u'gateway': u'10.24.64.126', u'traffictype': u'Guest', u'netmask': u'255.255.255.128', u'ipaddress': u'10.24.64.124', u'id': u'88ff7868-6fc6-4302-a7de-0cc9a9351ad9', u'isdefault': True}], u'cpuspeed': 2600, u'templateid': u'fc3863a1-d27d-4212-8241-f7d022e7d685', u'account': u'test', u'hostid': u'f1e89379-5fc2-4661-bd59-750991c2eecc', u'name': u'hadoop3', u'networkkbsread': 117598694, u'created': u'2014-07-25T17:59:18+0800', u'hypervisor': u'XenServer', u'rootdevicetype': u'NetworkFilesystem', u'rootdeviceid': 0, u'serviceofferingname': u'test-z2p201c1-4CPU-8G-secst', u'templatedisplaytext': u'jtcaiwuapp-rehl6.3-64-50G'}]
    num = 0
    cs = CloudStackClient(config)
    count = len(cs.list_all_vms())
    vms = cs.list_all_vms()
#    for obj in vms:
#        asset = {}
#        asset = asset_obj(obj)
#        rack_object_id = rack.check_RackObject(asset)
#        if rack_object_id:
#            print "{0}: {1}: {2} already exist ! skippped...".format(asset['obj_type'], rack_object_id, asset['cn_name']) 
#        else:
#            num += 1
#            rack_object_id = rack.add_object(asset)
#            rack.add_object(asset)
#            print('+ New rack_object created: {0}: {1}: {2}: {3}'.format(num, asset['obj_type'], rack_object_id, asset['cn_name']))
#            
    for obj in vms:
        asset = {}
        asset = Asset(obj)
        rack.add_ip(asset)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    main()
