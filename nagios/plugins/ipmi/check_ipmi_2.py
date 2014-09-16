#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Obtain informations by ipmi

import os
import sys
import argparse

# Exit statuses recognized by Nagios
UNKNOWN = -1
OK = 0
WARNING = 1
CRITICAL = 2
nagios = UNKNOWN
status = "unknown"

# tests pour le status nagios
def test(result,warning,critical) :
	'''Compare value with threshold to define nagios status'''

	 #comparaison avec les seuils
	if result >= critical :
	        nagios = CRITICAL
	elif warning <= result and result < critical :
        	nagios = WARNING
	else :
        	nagios = OK

	return nagios

#voir pour faire un test genre output d.j. d.fini ou pas pour .viter de la d.finit au pr.alable
output = ""
output_graph = ""

#gestion des arguments :
parser = argparse.ArgumentParser(description='Get ipmi informations for nagios',epilog="This plugin uses the 'ipmitool' command included with the OpenIPMI-tools package. if you don't have the package installed, you will need to download it from http://sourceforge.net/projects/openipmi/ before you can use this plugin.")
parser.add_argument('command',nargs='+',help='sensor(s) to question')
parser.add_argument("-H","--hostname",action="store",help='Host name or IP address')
parser.add_argument("-U","--username",action="store",help='Remote session username')
parser.add_argument("-P","--password",action="store",help='Remote session password')
parser.add_argument("-w","--warning",required=True,action="store",help='Warning threshold range(s)')
parser.add_argument("-c","--critical",required=True,action="store",help='Critical threshold range(s)')
parser.add_argument("-t","--threshold",action="store_true",help='Thresholds are present in output to be displayed in graph')
parser.add_argument('--version', action='version', version='%(prog)s 0.2')
args = parser.parse_args()

#interrogation ipmi
for i in args.command :
	result = os.popen("ipmitool -H %s -I lan -U %s -P %s sensor reading \"%s\"" % (args.hostname,args.username,args.password,i)).read().split('|')
	output = "%s,%s" % (output,result[1].strip())
	output_graph = "%s %s=%s" % (output_graph,result[0].strip(),result[1].strip())
	nagios = max(nagios,test(result[1].strip(),args.warning,args.critical))


if nagios == 0 :
	status = "OK"
elif nagios == 1 :
	status = "WARNING"
elif nagios == 2 :
	status = "CRITICAL"
elif nagios == -1 :
	status = "UNKNOWN"
else :
	status = "ERROR"

#formatage pour nagios
if args.threshold :
	print "IPMI %s : %s. | %s warning=%s critical=%s" % (status,output.strip(','),output_graph.strip(),args.warning,args.critical)
else :
	print "IPMI %s : %s. | %s" % (status,output.strip(','),output_graph.strip())
sys.exit(nagios)
