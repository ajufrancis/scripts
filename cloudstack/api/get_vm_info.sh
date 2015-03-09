#!/bin/bash
cd /srv/scripts/cloudstack
./get_internet-fw01_config.sh
./listVMs.py > vm_tables.html
