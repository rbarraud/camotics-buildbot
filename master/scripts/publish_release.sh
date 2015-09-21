#!/bin/bash

TARGET=root@coffland.com:/var/www/camotics.org/http/releases/

rsync -av --max-delete=-1 --progress /home/buildmaster/releases/ $TARGET
