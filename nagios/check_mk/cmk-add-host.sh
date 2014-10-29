#!/bin/bash
#usage: /tmp/cmk-add-host.sh sitename hostname
site=$1; shift
hostname=$1; shift

mk_file="/opt/omd/sites/$site/etc/check_mk/conf.d/wato/hosts.mk"
wato_file="$(dirname $mk_file)/.wato"

## exit with code 1 if host exists
(
cat <<EOT
GET hosts
Columns: host_name
EOT
) | su - $site -c "lq" \
  | grep -q $hostname
if [[ $? == 0 ]]; then
  echo "$hostname already added"
  exit 1
fi

grep -q $hostname /etc/hosts
if [[ $? != 0 ]]; then
  echo "$hostname failed to resolve"
  exit 1
fi

## add host to base wato hosts.mk
cat <<EOT >> $mk_file

all_hosts += [ "$hostname|$tags|wato|/" + FOLDER_PATH + "/" ]
host_attributes.update({'$hostname': {}})
EOT

## update num_hosts var for wato
current_num_hosts=$( cat $wato_file | sed -e "s/^.*'num_hosts': //" -e "s/,.*$//")
new_num_hosts=$(( $current_num_hosts + 1 ))
sed -i $wato_file -e "s/'num_hosts': [0-9]\+/'num_hosts': $new_num_hosts/"

#su - $site -c "cmk -II $hostname"

exit 0
