#!/bin/bash
NEW_SVC_LIST="new_svc.log"

test -z $1 && echo ERROR && exit 1

echo "config"
svc_ports="$1"

for i in `echo $svc_ports`
do
  echo "service tcp$i" >> $NEW_SVC_LIST

  echo "service tcp$i"
  echo "tcp dst-port $i src-port 1 65535"
done

echo "save"
