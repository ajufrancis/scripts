#!/bin/bash
# example: ./nat.sh jituanmis1 tcp 114.251.196.114 9061 192.168.32.161 9060

SVC_NAME="$1"
SVC_PROTO="$2"
SVC_DESC="$7"

FROM_IP="$3"
FROM_PORT="$4"

TO_IP="$5"
TO_PORT="$6"

########################################
cat <<EOF >> ./fw_rules/svc.rule
service ${SVC_NAME}${FROM_PORT}
  $SVC_PROTO dst-port $FROM_PORT src-port 1 65535
  desc "$SVC_NAME,$SVC_PROTO:from $FROM_PORT"
exit

EOF

cat <<EOF >> ./fw_rules/dnat.rule
nat
  dnatrule from any to $FROM_IP service ${SVC_NAME}${FROM_PORT} trans-to $TO_IP port $TO_PORT log
exit

EOF

cat <<EOF >> ./fw_rules/policy.rule
policy
rule
  action permit
  enable
  src-zone untrust
  dst-zone trust
  src-add any
  dst-ip ${FROM_IP}/32
  service "${SVC_NAME}-${SVC_PROTO}${FROM_PORT}"
  desc "$SVC_NAME,$SVC_PROTO:$FROM_PORT"
exit
exit

EOF
