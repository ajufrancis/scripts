#!/bin/bash
cd /home/nagios
msg=`cat /tmp/weixin.out`
cookie="mozilla/5.0 (windows nt 6.1; wow64) applewebkit/537.22 (khtml, like gecko) chrome/25.0.1364.97 safari/537.22"

version="weixin version 1.0 Sep 2013-08-21 written by eddie wen\n http://www.icanwen.com"

Echo="echo -e"

print_help_msg(){
	$Echo "Usage: $0 -h to get help."
}

print_full_help_msg(){
	$Echo "Usage:"
	$Echo "$0  -v print script version" 
	$Echo "$0  -h print help message"
	$Echo "$0  -f fakeid "
	$Echo "Example:"
	$Echo "${0} -m message -f fakeid"
}

print_version(){
	$Echo $version
}

if [ $# -lt 1 ]; then
	print_help_msg
	exit 3
else
	while getopts :vhf: OPTION
	do
		case $OPTION
			in
			f)
			FAKEID=$OPTARG
			;;
			v)
			print_version
			exit 3
			;;
			h)
			print_full_help_msg
			exit 3
			;;
			?)
			$Echo "Error: Illegal Option."
			print_help_msg
			exit 3
			;;
		esac
	done

fi


curl -F msg="$msg" -F fakeid="$FAKEID" --user-agent "$cookie" --cookie header_and_cookies --cookie-jar header_and_cookies http://nodejs_ip:8080/wx/login 
