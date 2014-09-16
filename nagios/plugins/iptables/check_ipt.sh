#!/bin/bash

#if cat /etc/issue
#IPT='/usr/sbin/iptables'
IPT='/sbin/iptables'
GREP='/bin/grep'
AWK='/bin/awk'
EXPR='/usr/bin/expr'
WC='/usr/bin/wc'

STAT=0
OUTPUT=''
CHAINS=`$IPT -nvL | $GREP 'Chain' | $AWK '{ print $2 }'`

for CHAIN in $CHAINS ; do
	if [ "$CHAIN" != 'FORWARD' ] && [ "$CHAIN" != 'OUTPUT' ] && [ `$EXPR substr $CHAIN 1 4` != "LOG_" ] ; then
		CNT=`expr $($IPT -S $CHAIN | $WC -l) '-' 1`
		if [ $CNT -eq 0 ] ; then
			OUTPUT="<b>${OUTPUT}ERROR $CHAIN $CNT rules!</b><br>"
			STAT=2
		else
			OUTPUT="${OUTPUT}OK $CHAIN $CNT rules<br>"
		fi
	fi
done

echo $OUTPUT

exit $STAT


