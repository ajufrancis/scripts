#!/usr/bin/env python
from rt_base import *
from rt_pprinter import *

dictionary = api('get_dictionary')
attributes = api('get_attributes')
rackspace = api('get_rackspace')
depot = api('get_depot')
