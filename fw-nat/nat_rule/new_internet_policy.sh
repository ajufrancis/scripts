#!/bin/bash
function internet_policy()
{
if [ $# -lt 2 ];then
    echo ERROR && exit 1
elif [ $# -ge 2 ];then
  echo "config"
  echo "policy"
  echo "rule"
  echo "src-zo un"
  echo "dst-zo tr"
  echo "src-add any"
  echo "dst-ip ${1}/32"

  shift
  for i in $*
  do
    echo "service ${1}"
    shift
  done

  echo "ac per"
  echo "enab"
  echo "end"
  echo ""
fi
}

#################
# command list
#################
#config
#address $addr 
#ip
#host
#range
#rename
#desc
#member
#no
#end
#save
