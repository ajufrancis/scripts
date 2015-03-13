#!/usr/bin/python
#coding:utf-8
#http://download.cloud.com/releases/3.0.3/api_3.0.3/TOC_Root_Admin.html
import api
import output
import domain, user, host, vm, network, zone, cluster, pod, volumn
#import template, iso, router, firewall, pool, systemvm, nat, serviceoffering, vlan, diskoffering, address, event, capacity, alert

cs = api.client()
domains = domain.list(cs)
zones = zone.list(cs)
pods = pod.list(cs)
clusters = cluster.list(cs)
hosts = host.list(cs)
vms = vm.list(cs)
users = user.list(cs)
networks = network.list(cs)
#output.pprinter(vms)
output.csv_objectip(vms)
