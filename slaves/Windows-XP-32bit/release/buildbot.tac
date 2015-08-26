# -*- python -*-
import os
from twisted.application import service
from buildbot.slave.bot import BuildSlave

basedir = r'C:\Documents and Settings\buildbot\camotics\release'
buildmaster_host = '172.16.0.1'
port = 9989
slavename = 'Windows-XP-32bit-release'
passwd = open(os.path.expanduser('~/slave_passwd.txt')).read().strip()
keepalive = 600
usepty = 0
umask = 022
maxdelay = 300
rotateLength = 1000000
maxRotatedFiles = None

application = service.Application('buildslave')
try:
  from twisted.python.logfile import LogFile
  from twisted.python.log import ILogObserver, FileLogObserver
  logfile = LogFile.fromFullPath("twistd.log", rotateLength=rotateLength,
                                 maxRotatedFiles=maxRotatedFiles)
  application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
except ImportError:
  # probably not yet twisted 8.2.0 and beyond, can't set log yet
  pass
s = BuildSlave(buildmaster_host, port, slavename, passwd, basedir,
               keepalive, usepty, umask=umask, maxdelay=maxdelay)
s.setServiceParent(application)

