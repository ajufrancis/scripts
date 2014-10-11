#!/bin/bash
salt -G 'os:XenServer' cmd.run 'xe vm-list params=' > /srv/scripts/cloudstack/vm_tables_xs.txt
