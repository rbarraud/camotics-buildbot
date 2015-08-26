import os
import re
import operator

from genshi.builder import tag
from trac.wiki.macros import WikiMacroBase
from trac.wiki.api import parse_args

base_url = '/releases'
base = '/var/www/camotics.com/http/releases'
release = 'public'
logo_size = 128
packages = [
    ['%(os)s', ['Windows'], ['Windows-XP-32bit']],

    ['Mac %(os)s', ['OSX'], ['OSX-10.6.4-64bit']],

    ['64-bit %(os)s', ['Debian', 'Mint', 'Ubuntu'], ['Debian-Testing-64bit']],
    ['32-bit %(os)s', ['Debian', 'Mint', 'Ubuntu'], ['Debian-Testing-32bit']],
    ['LinuxCNC 10.04', ['Ubuntu'], ['LinuxCNC-10.04-32bit']],
    ['Ubuntu Precise 12.04', ['Ubuntu'], ['Ubuntu-Precise-64bit']],

    ['%(os)s', ['RedHat', 'CentOS', 'Fedora'],
     ['CentOS-5.5-32bit', 'CentOS-5.3-64bit']],
]

default_exts = ['.deb', '.rpm', '.exe', '.dmg', '.mpkg.zip', '.pkg.zip']


class ReleasesMacro(WikiMacroBase):
    '''Inserts the current project releases into the wiki page.'''

    def do_release(self, build, project):
        results = []

        try: 
            subdir = ('%s/%s/%s/%s/v%s' % (
                    release, mode, project, build, self.version)).lower()
            path = base + '/' + subdir

            for name in os.listdir(path):
                if not name.startswith('latest.'): continue

                ext = None
                for x in self.exts:
                    if name.endswith(x): ext = x
                if not ext: continue

                filename = path + '/' + name
                if not os.path.islink(filename): continue

                filename = os.path.basename(path + '/' + os.readlink(filename))

                url = base_url + '/%s/%s' % (subdir, filename)

                m = re.match(r'(\w+[_-])+(?P<major>\d+)\.' +
                             r'(?P<minor>\d+)\.(?P<rev>\d+)' +
                             r'([_-](1[\._-])?(?P<arch>[^\.-]+))?', filename)
                major = m.group('major')
                minor = m.group('minor')
                rev = m.group('rev')
                version = (int(major), int(minor), int(rev))
                arch = m.group('arch')
                if not arch: arch = 'any'

                results.append((url, filename, version, project, arch))

        except: pass

        return results


    def expand_macro(self, formatter, name, args):
        global mode, release

        args, kw = parse_args(args)
        if 'release' in kw: release = kw['release']
        self.version = kw['version']

        if 'project' in kw: projects = [kw['project']]
        else: projects = kw['projects'].split(':')

        if 'mode' in kw: mode = kw['mode']
        else: mode = 'release'
        if 'exts' in kw: self.exts = filter(lambda x: x, kw['exts'].split(':'))
        else: self.exts = default_exts

        img_url = formatter.href.base + '/chrome/site/images'

        result = ''

        for desc, oses, builds in packages:
            items = []

            for project in projects:
                for build in builds:
                    items += self.do_release(build, project)

            if not len(items): continue

            # Find latest version
            max_version = (0, 0, 0)
            for item in items:
                if max_version < item[2]: max_version = item[2]

            # Filter out all but the latest version
            items = filter(lambda item: item[2] == max_version, items)

            # Find architectures
            archs = []
            for item in items:
                if not item[4] in archs: archs.append(item[4])

            result += '<div class="build">'
            desc %= {'os': ' / '.join(oses)}
            result += '<span class="build-desc">%s</span>' % desc
            for os in reversed(oses):
                result += '<div class="build-logo">'
                result += '<img src="%s/%s-%d.png"/>' % (
                    img_url, os.lower(), logo_size)
                result += '</div>'

            # Create links ordered by architecture
            for current_arch in archs:
                if 1 < len(archs):
                    result += '<div class="build-arch">%s:</div>' % (
                        current_arch)

                result += '<ul>'
                for url, filename, version, project, arch in items:
                    if current_arch == arch:
                        result += ('<li><a href="%s">%s</a></li>' % (
                                url, filename))
                result += '</ul>'

            result += '</div>'

        return result
