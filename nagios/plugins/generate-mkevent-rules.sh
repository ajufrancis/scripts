#!/bin/bash

cmk --list-hosts > cmk.host.list

cat <<EOF > ./mkevent.rules
# Written by script
# encoding: utf-8

rules += \
[
EOF

while read host
do
  cat << EOF >> ./mkevent.rules

{'actions': [],
  'autodelete': False,
  'count': {'algorithm': 'interval',
            'count': 1,
            'count_ack': False,
            'period': 604800,
            'separate_application': True,
            'separate_host': True,
            'separate_match_groups': True},
  'description': u'',
  'disabled': False,
  'drop': False,
  'hits': 0,
  'id': '$host',
  'match': u'.*',
  'match_host': u'$host',
  'set_contact': u'zhanghu',
  'sl': 0,
  'state': -1},
EOF
done < ./cmk.host.list

echo ']' >> mkevent.rules

sed -i -e '/^$/d' mkevent.rules
