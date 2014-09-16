#!/usr/bin/python
from optparse import OptionParser
from pyipmi import make_bmc
from pyipmi import tools
from pyipmi.bmc import LanBMC
from pyipmi.server import Server
 
"""
A simple script to power on/off a server using IPMI.
This uses pyipmi version 0.11.0.
 
Here is the help on this command line utility:
python power-ipmi.py -h
Usage: power-ipmi.py [options]
Example: ./power.py -H 192.168.10.1 -u ADMIN -p ipmiXSTEST2
 
Options:
  -h, --help            show this help message and exit
  -H HOST, --host=HOST  IP address of the BMC server
  -u USERNAME, --username=USERNAME
                        username
  -p PASSWORD, --password=PASSWORD
                        password
  -m MODE, --mode=MODE  power mode: on/off
"""
 
parser = OptionParser()
parser.add_option( "-H", "--host", dest="host", type=str, default="1.1.1.1",
                  help="IP address of the BMC server" )
parser.add_option( "-u", "--username", type=str, dest="username", default="default",
                  help="username" )
parser.add_option( "-p", "--password", type=str, dest="password", default="password",
                  help="password" )
parser.add_option( "-m", "--mode", type=str, dest="mode", default="on",
                  help="power mode: on/off" )
 
( args, op ) = parser.parse_args()
 
bmc = make_bmc( LanBMC, hostname=args.host, username=args.username, password=args.password, interface='lanplus' )

output = bmc.lan_print()
#print type(output)
info = tools.responseparser.ResponseParserMixIn.response_parser(output)
print info
#print type(info)
#print bmc.get_chassis_status()
#server = Server( bmc )
#if args.mode == "on":
#    print "Powering on the server."
#    server.power_on()
#    sleep(10)
#else:
#    print "Powering off the server."
#    server.power_off()
# 
# print "The server is in state: %s" % server.is_powered
