#!/bin/bash

TARGET=root@coffland.com:/var/www/camotics.org/http/releases/

rsync -av --max-delete=-1 /home/buildmaster/releases/ $TARGET
