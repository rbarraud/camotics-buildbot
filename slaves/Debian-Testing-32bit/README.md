# Initial
  * Install Debian system to VM
  * Create buildbot user
  * Add buildbot to group sudo
  * Login as buildbot
  * Install C! and CAMotics prerequisites (See CAMotics README.md)

# Build and install buildbot 0.7.10p2-jcoffland
```
mkdir ~/build
cd ~/build
git clone https://github.com/CauldronDevelopmentLLC/buildbot
cd buildbot
git checkout 0.7.10p2-jcoffland
sudo python setup.py install
```

# Setup slave
```
cd ~/build
git clone https://github.com/CauldronDevelopmentLLC/buildbot-config
ln -s ~/build/buildbot-config/slaves/Debian-Testing-32bit ~/camotics
vi ~/slave_passwd.txt # Enter slave password and save
```

# Start slaves
```
cd ~/camotics/debug
make start
cd ../release
make start
```
