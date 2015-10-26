#!/bin/bash

SRC=/home/buildmaster/releases
DST=root@coffland.com:/var/www/camotics.org/http/releases

read -sp "Password: " PASS

for MODE in release debug; do
    sshpass -p "$PASS" \
        rsync -av --max-delete=-1 --progress $SRC/public/$MODE/camotics/ \
        $DST/public/$MODE/camotics/
done
