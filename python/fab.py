#!/usr/bin/env python
from fabric.api import run, execute ,env

class Fetcher:
  def __init__(self,hosts=[]):
    env.hosts= hosts
    env.warn_only = True  # needed to not abort on pingtimout or other errs

  def getclock(self)
    run('sh clock')

  def fetch(self):
    results = execute(self.getclock,hosts=env.hosts)


if __name__ == '__main__':
  hosts = loadfromtxt(hosts.txt)
  f = Fetcher(hosts=hosts)
  f.fetch()
