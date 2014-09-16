#!/bin/bash
# used for xenserver 6.0.2 with updates installed
# check if pool's primary storage repository is mounted as /root/.nfsmounts expected
# if /root/.nfsmounts lost, save current nfsmounts to it, and mount them

nfsmounts="/root/.nfsmounts"
save_mounts(){
  if [ ! -f $nfsmounts ];then
    echo "$nfsmounts lost, write new info to $nfsmounts !"
    grep nfs /proc/mounts | grep -v template | grep -v snapshot | awk '/addr/ { print $1,$2}' > $nfsmounts
  fi
}

mount_nfs() {
  opt="rw,soft,timeo=133,tcp,actimeo=0"
  if [ -f $nfsmounts ];then
    while read line
    do
      grep -q $line /proc/mounts
      if [ $? -eq 1 ];then
        echo "$line not mounted"
        echo "RUN CMD: mount -t nfs -o $opt $line"
        mount -t nfs -o $opt $line
      fi
    done < $nfsmounts
  else
    echo "$nfsmounts lost!"
  fi
}

save_mounts
mount_nfs
