#!/usr/bin/python
import os, sys
import salt.client

local = salt.client.LocalClient()
grains = local.cmd('pxe', 'grains.items')
print grains
