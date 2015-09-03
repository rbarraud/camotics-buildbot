password = open('passwd.txt').read().strip()

# Debian
add_slave('Debian-Testing-32bit', password, 'lin', '~/camotics',
          configs = ['release', 'debug'])

add_slave('Debian-Testing-64bit', password, 'lin', '~/camotics',
          configs = ['release', 'debug'])

# LinuxCNC
add_slave('LinuxCNC-10.04-32bit', password, 'lin', '~/camotics',
          configs = ['release', 'debug'])

# Ubuntu
add_slave('Ubuntu-Precise-64bit', password, 'lin', '~/camotics',
          configs = ['release', 'debug'])

# Windows
add_slave('Windows-XP-32bit', password, 'win',
          'c:\\buildbot-config\\slaves\\Windows-XP-32bit',
          configs = ['release', 'debug'])

# OSX
add_slave('OSX-10.6.4-64bit', password, 'osx', '~/camotics',
          configs = ['release', 'debug'])
