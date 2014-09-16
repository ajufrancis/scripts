$template wallmsg,"\r\n\7Message from syslogd@%HOSTNAME% at %timegenerated% ...\r\n %syslogtag%%msg%\n\r"
:msg, contains, "bla"    ^echo $msg | send_nsca -c /etc/send_nsca.cfg ;bla_logged
