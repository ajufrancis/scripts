osc2rack
========

ocs2rack is an append only (non destructive) import tool for [RackTables][1].
ocs2rack translate assets stored in [OCS-Inventory][2] and import them into RackTable.

ocs2rack was written and tested with ocsinventory-server v.1.01 and RackTables v.0.19.9

  [1]: http://racktables.org/
  [2]: http://www.ocsinventory-ng.org/en/

Install
=======

Python module dependency:

 - IPy
 - MySQLdb


Configuration
=============

ocs2rack use a configuration file (default is ocs2rack.conf).
The configuration file can be given by OCS2RACK_CONFIG environnement variable,
or as command line argument.

Copy ocs2rack.conf.sample to ocs2rack.conf and adjust it to fit your need.
   
Usage
=====


    $ python ocs2rack.py
    (...)
    Processing OCS asset #1337 (494/745): "sc01" 
            +New rack_object id #543 created
            +New TAG #47 "SQUIDCACHE" added
            +rack_objet TAGed as "SQUIDCACHE"
            +Port (Ethernet) "eth0" added
            +IP address "172.19.32.1" added.
            #No FQDN, trying to reverse from IP "172.19.32.1"
            +Attribute fqdn: "sc01.xxxx.fr" added.
            +Attribute dranm_mb: "16085" added.
            +Attribute cpu_mhz: "2333" added
            +Attribute sw_version: "Debian / 5.0.6 / #1 SMP Wed Mar 4 13:01:51 CET 2009" added
            +Attribute oem_sn1: "CZJ7290ABC" added
            +Attribute hw_type: "ocs2rack%GPASS%ProLiant DL360 G5" added
            +Attribute sw_type: "ocs2rack%GPASS%Linux" added
    
    Processing OCS asset #1672 (495/745): "sc02" 
            +New rack_object id #544 created
            +rack_objet TAGed as "SQUIDCACHE"
            +Port (Ethernet) "eth0" added
            +IP address "172.18.16.2" added.
            #No FQDN, trying to reverse from IP "172.18.16.2"
            ! reverse "172.18.16.2": [Errno 1] Unknown host
            +Attribute dranm_mb: "16085" added.
            +Attribute cpu_mhz: "2333" added
            +Attribute sw_version: "Debian / 5.0.6 / #1 SMP Wed Mar 4 13:01:51 CET 2009" added
            +Attribute oem_sn1: "CZJ7280ABC" added
            +Attribute hw_type: "ocs2rack%GPASS%ProLiant DL360 G5" added
            +Attribute sw_type: "ocs2rack%GPASS%Linux" added
    (...)
