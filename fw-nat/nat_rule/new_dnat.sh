#!/bin/bash

if [ $# -lt 2 ];then
  echo ERROR && exit 1
fi

echo "config"
echo "nat"
echo "dnat from any to $1 trans-to $2"
echo -e "end\n"
echo ""
