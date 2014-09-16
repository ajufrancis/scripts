#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
ocs2rack is an append only (non destructive) import tool for RackTables.
ocs2rack translates assets stored in OCS-Inventory and import them into RackTables.
'''

#-- 2011-09-28, Stéphane Bunel
#--           * Initial creation
#--           * Dependency: ipy (http://pypi.python.org/pypi/IPy/)
#--             Debian/Ubuntu: apt-get install python-ipy
#-- 2011-10-05, Stéphane Bunel
#--           * Add configuration file (default: ocs2rack.conf)
#--           * Tested with 700+ assets
#-- 2013-09-18, Stéphane Bunel
#--           * add_attribute_value() is now comptible with new
#--             racktables DB schema. Tested with racktables v0.20.5

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
        'ocs2rack need python module MySQLdb: {0}'.format(sys.exc_info()[1]))
    sys.exit(1)

try:
    from IPy import IP
except:
    print('ocs2rack need python module IPy: {0}'.format(sys.exc_info()[1]))
    sys.exit(1)


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

    def check_object(self, name):
        sql = '''SELECT id FROM RackObject WHERE name = %s AND objtype_id = %s'''
        self._curs.execute(sql, (name, 4))
        if self._curs.rowcount:
            return self._curs.fetchone()['id']
        return 0

    def add_object(self, name, label='', asset=None, pb='no', comment=None):
        sql = '\n'.join([
            'INSERT INTO RackObject',
            '    ( name, label, objtype_id, asset_no, has_problems, comment )',
            'VALUES',
            '    ( %s, %s, %s, %s, %s, %s )',
        ])
        self._curs.execute(sql, (name, label, 4, asset, pb, comment))
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

    def check_add_ip_allocation(self, rack_object_id, name, ip_addr):
        ipnet = IP(ip_addr)
        ip_dec = int(ipnet.strDec())

        sql_check = '''SELECT 1 FROM {0} WHERE object_id = %s AND ip = %s AND name = %s AND type = %s'''
        sql_add = '\n'.join([
            'INSERT IGNORE INTO {0}',
            '    ( object_id, ip, name, type )',
            'VALUES',
            '    ( %s, %s, %s, %s )'
        ])

        if ipnet.version() == 6:
            sql_check = sql_check.format('IPv6Allocation')
            sql_add = sql_add.format('IPv6Allocation')
        else:
            sql_check = sql_check.format('IPv4Allocation')
            sql_add = sql_add.format('IPv4Allocation')

        if name.startswith('lo'):
            if_type = 'virtual'
        else:
            if_type = 'regular'

        self._curs.execute(
            sql_check, (rack_object_id, ip_dec, name, if_type))
        if self._curs.rowcount:
            return 0

        self._curs.execute(sql_add, (rack_object_id, ip_dec, name, if_type))
        return self._curs.rowcount

    def check_add_port(self, rack_object_id, name, iif_id=1, p_type=24,
                       l2address='', reservation_comment=''):

        sql_check = '''SELECT 1 FROM Port WHERE object_id = %s AND name = %s'''
        sql_add = '\n'.join([
            'INSERT INTO Port',
            '    ( object_id, name, iif_id, type, l2address, reservation_comment )',
            'VALUES',
            '    ( %s, %s, %s, %s, %s, %s )',
        ])

        self._curs.execute(sql_check,
                          (rack_object_id, name))
        if self._curs.rowcount:
            return 0

        self._curs.execute(sql_add,
                          (rack_object_id, name, iif_id, p_type, l2address, reservation_comment))
        return self._curs.lastrowid

    def fetch_tag(self, name):
        sql = 'SELECT id FROM TagTree WHERE tag = %s'
        self._curs.execute(sql, (name))
        r = self._curs.fetchone()
        if r:
            return r['id']
        return None

    def add_tag(self, name):
        sql = 'INSERT INTO TagTree ( tag ) VALUES ( %s )'
        self._curs.execute(sql, (name))
        return self._curs.lastrowid

    def add_tag_to_object(self, object_id, tag_id):
        sql = 'INSERT IGNORE INTO TagStorage ( entity_id, tag_id ) VALUES ( %s, %s )'
        self._curs.execute(sql, (object_id, tag_id))
        if self._curs.rowcount:
            return True
        return False

    def check_attribute_value(self, rack_object_id, attr_id):
        sql = 'SELECT 1 FROM AttributeValue WHERE object_id = %s AND attr_id = %s'
        self._curs.execute(sql, (rack_object_id, attr_id))
        if self._curs.rowcount:
            return True
        return False

    def add_attribute_value(self, rack_object_id, attr_id, val):
        object_tid = 4  # This is the default object type for new objects.
                        # From table Dictionaty (dict_key = 4) it means
                        # "Server".
        sql = 'SELECT id, type FROM Attribute WHERE id = %s'
        self._curs.execute(sql, (attr_id))
        attr_type = self._curs.fetchone()['type']
        sql = 'INSERT IGNORE INTO AttributeValue ( object_id, object_tid, attr_id, '
        if attr_type == 'string':
            sql += 'string_value'
        elif attr_type == 'uint':
            sql += 'uint_value'
        elif attr_type == 'float':
            sql += 'float_value'
        elif attr_type == 'dict':
            sql += 'uint_value'
        sql += ' ) VALUES ( %s, %s, %s, %s )'
        self._curs.execute(sql, (rack_object_id, object_tid, attr_id, val))
        if self._curs.rowcount:
            return True
        return False

    def add_to_dictionary(self, chapter, value):
        sql_select = 'SELECT dict_key FROM Dictionary WHERE chapter_id = %s AND dict_value = %s'
        sql_insert = 'INSERT INTO Dictionary ( chapter_id, dict_value ) VALUES ( %s, %s )'
        self._curs.execute(sql_select, (chapter, value))
        if self._curs.rowcount:
            return self._curs.fetchone()['dict_key']
        self._curs.execute(sql_insert, (chapter, value))
        return self._curs.lastrowid

    def append(self, asset):
        asset.get_info('bios')
        asset.get_info('networks')
        asset.get_info('accountinfo')

        try:
            bios = asset.bios[0]
        except:
            print(
                '''BIOS informations are not availables. That's BAD for me.''')
            return

        ocs_hardware_id = asset.ID

        #-- Is server already exists in rack ?
        rack_object_id = self.check_object(asset.NAME)
        if not rack_object_id:
            comment = '---\nocs2rac: ocs.hardward.id={0}\n'.format(
                ocs_hardware_id)
            for k in (
                    'OSNAME', 'OSVERSION:', 'OSCOMMENTS',
                    'PROCESSORT', 'PROCESSORS', 'PROCESSORN', 'MEMORY',
                    'SWAP', 'DESCRIPTION', 'SSN'):
                comment += '{0}: {1}\n'.format(
                    k, asset.__dict__.get(k, 'N/A'))
            comment += '\n-- BIOS --\n'

            for k in (
                    'SMANUFACTURER', 'SMODEL', 'SSN', 'TYPE', 'BMANUFACTURER',
                    'BVERSION', 'BDATE'):
                comment += '{0}: {1}\n'.format(k, bios.get(k, 'N / A'))

            rack_object_id = self.add_object(
                name=asset.NAME, comment=comment)
            print(
                '\t+New rack_object id #{0} created'.format(rack_object_id))

        #-- Add TAGS:
        if self._config.get_bool('rack', 'import_tag'):
            for ocs_tag in asset.accountinfo:
                tag_id = self.fetch_tag(ocs_tag['TAG'])
                if not tag_id:
                    tag_id = self.add_tag(ocs_tag['TAG'])
                    print('\t+New TAG #{1} "{0}" added'.format(
                        ocs_tag['TAG'], tag_id))
                added = self.add_tag_to_object(rack_object_id, tag_id)
                if added:
                    print(
                        '\t+rack_objet TAGed as "{0}"'.format(ocs_tag['TAG']))

        #-- Process network stuff
        first_eth_ip = None
        for port in asset.networks:

            ip_addr, ip_net = port.get('IPADDRESS'), port.get('IPMASK')

            #-- Check/Add network (ip/len)
            if ip_addr and not ip_addr.startswith('127') and not ip_addr.startswith('::1'):
                try:
                    if self.check_add_ip_network(ip_addr, ip_net):
                        print(
                            '\t+New NETWORK "{0}/{1}" added.'.format(ip_addr, ip_net))
                except:
                    print('\t! NETWORK "{0}/{1}": {2}'.format(
                        ip_addr, ip_net, sys.exc_info()[1]))

            #-- Check/Add physical port
            if ip_addr and not ip_addr.startswith('127') and not ip_addr.startswith('::1'):
                p_type = 440  # -- unknown
                type_to_type = {
                    'Ethernet':         24,  # -- Arbitrarily 1000 BaseTX
                    'Point-to-Point':   19,  # -- Arbitrarily 100Base-TX
                    'Local':            1469,  # -- Virtual port
                }
                if port['TYPE'] in type_to_type:
                    p_type = type_to_type[port['TYPE']]
                else:
                    print('\t! Unknown port type: {0}'.format(port['TYPE']))

                oid = self.check_add_port(
                    rack_object_id,
                    name=port['DESCRIPTION'],
                    iif_id=1,  # -- Hardwired
                    p_type=p_type,
                    l2address=port['MACADDR'],
                )
                if oid:
                    print('\t+Port ({1}) "{0}" added'.format(
                        port['DESCRIPTION'], port['TYPE']))

            #-- Check/Add IP to rack object
            try:
                if ip_addr and not ip_addr.startswith('127') and not ip_addr.startswith('::1'):
                    if not first_eth_ip and not port['DESCRIPTION'].startswith('lo'):
                        first_eth_ip = ip_addr
                    if self.check_add_ip_allocation(rack_object_id, port['DESCRIPTION'], ip_addr):
                        print('\t+IP address "{0}" added.'.format(ip_addr))
            except:
                print(
                    '\t! Add ip allocation: {0}'.format(sys.exc_info()[1]))

        #-- Add attributes
        #-- FQDN:
        if first_eth_ip and self._config.get_bool('rack', 'resovle_fqdn'):
            if not self.check_attribute_value(rack_object_id, self.ATTR_FQDN):
                print(
                    '\t#No FQDN, trying to reverse from IP "{0}"'.format(first_eth_ip))
                fqdn = None
                try:
                    fqdn = socket.gethostbyaddr(first_eth_ip)[0]
                except:
                    print('\t! reverse "{0}": {1}'.format(
                        first_eth_ip, sys.exc_info()[1]))
                if fqdn:
                    added = self.add_attribute_value(
                        rack_object_id, self.ATTR_FQDN, fqdn)
                    if added:
                        print('\t+Attribute fqdn: "{0}" added.'.format(fqdn))

        #-- DRAM_MB:
        try:
            ram_mb = int(asset.MEMORY)
            if ram_mb:
                added = self.add_attribute_value(
                    rack_object_id, self.ATTR_DRAM_MB, ram_mb)
                if added:
                    print(
                        '\t+Attribute dranm_mb: "{0}" added.'.format(ram_mb))
        except:
            pass

        #-- CPU_MHZ
        try:
            cpu_mhz = int(asset.PROCESSORS)
            if cpu_mhz:
                added = self.add_attribute_value(
                    rack_object_id, self.ATTR_CPU_MHZ, cpu_mhz)
                if added:
                    print(
                        '\t+Attribute cpu_mhz: "{0}" added'.format(cpu_mhz))
        except:
            pass

        #-- SW_VERSION:
        try:
            sw_version = asset.OSCOMMENTS
            if sw_version:
                added = self.add_attribute_value(
                    rack_object_id, self.ATTR_SW_VERSION, sw_version)
                if added:
                    print(
                        '\t+Attribute sw_version: "{0}" added'.format(sw_version))
        except:
            pass

        #-- OEM_SN1:
        try:
            oem_sn1 = bios['SSN']
            if oem_sn1:
                added = self.add_attribute_value(
                    rack_object_id, self.ATTR_OEM_SN1, oem_sn1)
                if added:
                    print(
                        '\t+Attribute oem_sn1: "{0}" added'.format(oem_sn1))
        except:
            pass

        #-- HW_TYPE
        if self._config.get_bool('rack', 'import_hw_type'):
            hw_type = bios['SMODEL']
            if hw_type:
                #-- chapter 11 = server models
                value = 'ocs2rack%GPASS%{0}'.format(hw_type)
                dict_key = self.add_to_dictionary(chapter=11, value=value)
                added = self.add_attribute_value(
                    rack_object_id, self.ATTR_HW_TYPE, dict_key)
                if added:
                    print('\t+Attribute hw_type: "{0}" added'.format(value))

        #-- SW_TYPE
        if self._config.get_bool('rack', 'import_sw_type'):
            sw_type = asset.OSNAME
            if sw_type:
                #-- chapter 13 = server OS type
                value = 'ocs2rack%GPASS%{0}'.format(sw_type)
                dict_key = self.add_to_dictionary(chapter=13, value=value)
                added = self.add_attribute_value(
                    rack_object_id, self.ATTR_SW_TYPE, dict_key)
                if added:
                    print('\t+Attribute sw_type: "{0}" added'.format(value))


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class OCS(object):

    def __init__(self, config):
        self._config = config
        self.asset_ids = None  # -- List of asset to process

        try:
            self._db = MySQLdb.connect(
                host=config.get('ocs', 'db_host'),
                db=config.get('ocs', 'db_name'),
                user=config.get('ocs', 'db_user'),
                passwd=config.get('ocs', 'db_pass'),
                use_unicode=True,
                cursorclass=MySQLdb.cursors.DictCursor)
        except:
            print(sys.exc_info()[1])
            sys.exit(1)

        self._db.autocommit(True)
        self._curs = self._db.cursor()

    def assets(self):
        sql = '''SELECT id FROM hardware'''
        args = list()
        try:
            rbd = self._config.get('ocs', 'reject_before_date')
            sql += ''' WHERE lastdate >= %s'''
            args.append(rbd)
        except ConfigParser.NoOptionError:
            pass
        try:
            limit = self._config.get_int('ocs', 'process_max')
            sql += ''' LIMIT %s'''
            args.append(limit)
        except ConfigParser.NoOptionError:
            pass
        self._curs.execute(sql, args)
        asset_ids = [i['id'] for i in self._curs.fetchall()]
        return OCSAssets(self, asset_ids)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class OCSAssets(object):

    def __init__(self, ocs_modele, asset_ids):
        self._model = ocs_modele
        self._asset_ids = asset_ids
        self._id = None  # -- current asset_id
        self.count = len(asset_ids)

    def __iter__(self):
        return self

    def next(self):
        if not self._asset_ids:
            raise StopIteration
        self._id = self._asset_ids.pop(0)
        sql = '''SELECT * FROM hardware WHERE id = %s'''
        self._model._curs.execute(sql, (self._id))
        self.__dict__.update(self._model._curs.fetchone())
        return self

    def get_info(self, table):
        sql = '''SELECT * FROM {0} WHERE hardware_id = %s'''.format(table)
        self._model._curs.execute(sql, (self._id))
        self.__dict__[table] = self._model._curs.fetchall()
        return self


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    config = Config()
    rack = RACK(config)
    ocs = OCS(config)

    for nb, asset in enumerate(ocs.assets()):
        if True:  # asset.ID == 1791:
            print('\nProcessing OCS asset #{3} ({1}/{2}): "{0}" '.format(
                asset.NAME, nb + 1, asset.count, asset.ID))
            rack.append(asset)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    main()
