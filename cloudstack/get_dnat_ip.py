#!/usr/bin/python
# coding=UTF-8
import sys, os
import re

def get_latest_file():
  with open('./nat/config.conf') as f:
    latest_file = f.readline().strip('\n')
    latest_file = latest_file.split('/')[-1]
    latest_file = './nat/' + latest_file
    return latest_file

def get_dnat_ip(ip):
  latest_file = get_latest_file()

  ips = []
  with open(latest_file) as f:
    for line in f.readlines():
      line = line.replace('"','')
      line = line.strip('\n')
      line = line.strip(' ')
      if 'dnatrule' in line:
        line = re.sub(r".*dnatrule.* to ", '', line)
        line = re.sub(r"track-tcp", '', line)
        line = re.sub(r"track-ping", '', line)
        line = re.sub(r"log", '', line)
        line = line.strip(' ')
        if ip in line.split(' '):
          ips += [line]
  return ips
