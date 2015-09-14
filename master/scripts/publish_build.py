#!/usr/bin/python

import sys
import os
import re
import shutil
import inspect

dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
execfile(dir + '/common.py')

root = '/home/buildmaster/builds'

# Parse args
if len(sys.argv) != 5:
    print 'Usage: %s <package> <slave name> <svn rev> <svn build>' % sys.argv[0]
    sys.exit(1)

package, slave_name, svn_rev, svn_build = sys.argv[1:5]

filename = os.path.basename(package)
project, major, minor, rev = parse_package_version(filename)

slave, mode = parse_slave_name(slave_name)

project = project.replace('_', '-').lower()
slave = slave.replace('_', '-').lower()
mode = mode.lower()

url = '%s/%s/%s/v%s.%s' % (mode, project, slave, major, minor)
base = '%s/%s' % (root, url)
svn_rev_dir = 'r%s-b%s' % (svn_rev, svn_build)
dir = '%s/%s' % (base, svn_rev_dir)
url = '%s/%s' % (url, svn_rev_dir)
latest = '%s/latest' % base

# Make dir
ensure_dir(dir)

# Move
#print 'mv %s %s' % (package, dir)
publish_file(package, dir, True)
os.unlink(package)
print '%s/%s' % (url, filename)

# Link latest dir
#print 'ln -sf %s %s' % (svn_rev_dir, latest)
force_link(svn_rev_dir, latest)

# Link latest package
latest += get_extension(filename)
latest_package = '%s/%s' % (svn_rev_dir, filename)
#print 'ln -sf %s %s' % (latest_package, latest)
force_link(latest_package, latest)

# Remove old files
revDirRE = re.compile(r'^r(?P<rev>\d+)-b(?P<build>\d+)$')
rev_dirs = []
for name in os.listdir(base):
    m = revDirRE.match(name)
    if m: rev_dirs.append(name)

if 10 < len(rev_dirs):
    def compare_rev_dirs(x, y):
        m1 = revDirRE.match(x)
        rev1, build1 = m1.groups(['rev', 'build'])
        m2 = revDirRE.match(y)
        rev2, build2 = m2.groups(['rev', 'build'])

        if int(rev1) == int(rev2): return int(build2) - int(build1)
        return int(rev2) - int(rev1)

    rev_dirs = sorted(rev_dirs, cmp = compare_rev_dirs)

    # Delete old revisions
    for dir in rev_dirs[10:]:
        shutil.rmtree(base + '/' + dir, ignore_errors = True)
