#!/bin/bash

SRC=/home/buildmaster/releases
DST=root@coffland.com:/var/www/camotics.org/http/releases

eval $(ssh-agent)

for MODE in release debug; do
    rsync -av --max-delete=-1 --progress $SRC/public/$MODE/camotics \
        $DST/public/$MODE/camotics
done

kill $SSH_AGENT_PID
