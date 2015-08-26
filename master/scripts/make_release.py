#!/usr/bin/python

import sys
import os
import re
import shutil
import inspect
import glob
from optparse import OptionParser

dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
execfile(dir + '/common.py')

build_base = '/var/www/camotics.com/builds'
release_base = '/var/www/camotics.com/http/releases'

releases = {
    'alpha': (build_base, release_base + '/alpha'),
    'beta': (release_base + '/alpha', release_base + '/beta'),
    'public': (release_base + '/beta', release_base + '/public'),
    }


# Parse command line
usage = 'Usage: %prog [options] <project> <version> <release>'
parser = OptionParser(usage = usage)
parser.add_option('-f', '--force', help = 'Force overwrite', default = False,
                  action = 'store_true', dest = 'force')
parser.add_option('-b', '--build', help = 'Build mode, release or debug',
                  default = None, dest = 'build_mode', type = 'choice',
                  choices = ['release', 'debug'])
parser.add_option('', '--test', help = 'Just print what would be done.',
                  default = False, action = 'store_true', dest = 'test')
options, args = parser.parse_args()


def find_builds(src, mode, project, version):
    base = '%s/%s/%s' % (src, mode, project)
    for build in os.listdir(base):
        fullpath = base + '/' + build

        if os.path.isdir(fullpath) and \
                re.match(r'^[^-]+-[^-]+-[^-]+$', build) and \
                os.path.isdir('%s/v%s' % (fullpath, version)):
            yield build


def publish_latest(path, target):
    if not options.test:
        if not publish_file(path, target, options.force): return False

        # Link latest
        ext = get_extension(path)
        force_link(os.path.basename(path), '%s/latest%s' % (target, ext))

    print 'Installed %s to %s' % (path, target)

    return True


def publish_builds(src, dst, project, version):
    if options.build_mode is not None: modes = [options.build_mode]
    else: modes = ['release', 'debug']

    for mode in modes:
        for build in find_builds(src, mode, project, version):
            base = '%s/%s/%s' % (src, mode, project)
            path = '%s/%s/v%s' % (base, build, version)
            target = '%s/%s/%s/%s/v%s' % (dst, mode, project, build, version)

            if os.path.islink(path + '/latest'): paths = [path + '/latest'] 
            else: paths = glob.glob(path + '/latest*')

            for latest in paths:
                if not os.path.islink(latest): continue
                latest = os.path.realpath(latest)

                if os.path.isdir(latest):
                    for name in os.listdir(latest):
                        publish_latest(latest + '/' + name, target)
                else: publish_latest(latest, target)



# Process args
if len(args) != 3: parser.error('Missing positional arguments')

project, version, release = args
project = project.lower()

if not release in releases: parser.error('Invalid release mode "%s"' % release)


# Publish builds
src, dst = releases[release]
publish_builds(src, dst, project, version)
