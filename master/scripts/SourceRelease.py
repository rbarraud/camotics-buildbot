import os
import re
import operator

from genshi.builder import tag
from trac.wiki.macros import WikiMacroBase
from trac.wiki.api import parse_args

base_url = '/releases'
base = '/var/www/camotics.com/http/releases'
release = 'public'
build = 'Debian-Testing-64bit'
logo_size = 128
default_exts = ['.tar.bz2']


class SourceReleasesMacro(WikiMacroBase):
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
        global mode, release, build

        args, kw = parse_args(args)
        if 'release' in kw: release = kw['release']
        self.version = kw['version']

        if 'project' in kw: projects = [kw['project']]
        else: projects = kw['projects'].split(':')

        if 'mode' in kw: mode = kw['mode']
        else: mode = 'release'

        if 'exts' in kw: self.exts = filter(lambda x: x, kw['exts'].split(':'))
        else: self.exts = default_exts

        if 'build' in kw: build = kw['build']

        img_url = formatter.href.base + '/chrome/site/images'

        result = ''
        items = []
        for project in projects:
            items += self.do_release(build, project)

        if not len(items): return '<h1>Empty Result</h1>'

        # Find latest version
        max_version = (0, 0, 0)
        for item in items:
            if max_version < item[2]: max_version = item[2]

        # Filter out all but the latest version
        items = filter(lambda item: item[2] == max_version, items)

        # Create HTML
        result += '<div class="build">'
        result += '<span class="build-desc">Source</span>'
        result += '<div class="build-logo">'
        result += '<img src="%s/source-%d.png"/>' % (img_url, logo_size)
        result += '</div>'

        result += '<ul>'
        for url, filename, version, project, arch in items:
            result += ('<li><a href="%s">%s</a></li>' % (url, filename))
        result += '</ul>'

        result += '</div>'

        return result
