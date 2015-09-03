# -*- python -*-
import os

from twisted.application import service
from buildbot.slave.bot import BuildSlave

basedir = os.getcwd()
buildmaster_host = '172.16.0.1'
port = 9989
slavename = os.environ['SLAVE_NAME']
passwd = open('passwd.txt', 'r').read().strip()
keepalive = 600
usepty = 0
umask = 022
maxdelay = 300

application = service.Application('buildslave')
s = BuildSlave(buildmaster_host, port, slavename, passwd, basedir,
               keepalive, usepty, umask=umask, maxdelay=maxdelay)
s.setServiceParent(application)

