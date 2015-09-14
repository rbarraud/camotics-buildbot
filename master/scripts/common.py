import re
import os
import grp
import pwd
import shutil
import filecmp

owner = 'buildmaster'
group = 'buildmaster'


def parse_package_version(name):
    m = re.match(r'(?P<project>[\w_-]+)[_-]'
                 r'(?P<major>\d+)\.(?P<minor>\d+)\.(?P<rev>\d+)[\._-]', name)
    if not m:
        raise Exception, "Failed to parse package version '%s'" % name

    return m.group('project', 'major', 'minor', 'rev')


def parse_slave_name(name):
    m = re.match(r'(?P<slave>[^_-]+[_-][^_-]+[_-][^_-]+)[_-]'
                 r'(?P<mode>[a-z]+)$', name)

    if not m:
        raise Exception, "Failed to parse slave name '%s'" % name

    return m.group('slave', 'mode')


def parse_package_name(name):
    m = re.match(r'(?P<project>[\w_-]+)[_-]'
                 r'(?P<major>\d+)\.(?P<minor>\d+)\.(?P<rev>\d+)[_-]'
                 r'(?P<slave>[^_-]+[_-][^_-]+[_-][^_-]+)[_-]'
                 r'(?P<mode>[a-z]+)'
                 r'(?P<arch>[_-][^.]+)?'
                 r'(?P<ext>\..*)$', name)
    if not m:
        raise Exception, "Failed to parse package name '%s'" % name

    return m.group('project', 'major', 'minor', 'rev', 'slave', 'mode', 'ext')


def correct_perms(file):
    if os.path.isdir(file): os.chmod(file, 0750)
    else: os.chmod(file, 0640)
    os.lchown(file, -1, grp.getgrnam(group)[2]) # must be member of the group


def ensure_dir(path):
    dir = ''
    for part in path.split('/'):
        dir += '/' + part
        if not os.path.exists(dir):
            os.mkdir(dir, 0750)
            correct_perms(dir)


def force_link(src, dst):
    if os.path.islink(dst): os.remove(dst)
    os.symlink(src, dst)
    correct_perms(dst)


def publish_file(src, target, force):
    if os.path.isdir(target): dst = target + '/' + os.path.basename(src)
    else: dst = target

    if os.path.exists(dst):
        if filecmp.cmp(src, dst): return False # Files are the same

        if not force:
            print '\033[91m"%s" already exists.\033[0m' % dst
            return False

    ensure_dir(target)
    shutil.copy(src, target)
    file = target + '/' + os.path.basename(src)
    correct_perms(file)

    return True


def get_extension(filename):
    m = re.match(r'^([^-_]*[-_])*[^-_.]+(?P<ext>\.[^-_]+)$', filename)
    if m: return m.group('ext')
    return ''
