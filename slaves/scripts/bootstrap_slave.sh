#!/bin/bash

while [ ${#} -gt 0 ]; do
    case $1 in
        -n) SLAVE_NAME="$2"; shift ;;
        -p) SLAVE_PASS="$2"; shift ;;
        -m) SLAVE_MODE="$2"; shift ;;
    esac

    shift
done

if [ "$SLAVE_NAME" == "" ]; then echo "SLAVE_NAME not set"; exit 1; fi
if [ "$SLAVE_PASS" == "" ]; then echo "SLAVE_PASS not set"; exit 1; fi
if [ "$SLAVE_MODE" == "" ]; then echo "SLAVE_MODE not set"; exit 1; fi

SLAVE="$SLAVE_NAME/$SLAVE_MODE"
if [ ! -d "/host/$SLAVE" ]; then
    echo "Cannot find slave directory /host/$SLAVE"
    exit 1
fi

# Setup slave
mkdir -p /slave/$SLAVE/info
touch /slave/$SLAVE/info/host
echo "Joseph Coffland <jcoffland@cauldrondevelopment.com>" \
    > /slave/$SLAVE/info/admin
cp -av /host/$SLAVE/* /slave/$SLAVE
echo "$SLAVE_PASS" >/slave/$SLAVE/passwd.txt
export NCORES=$(grep -c ^processor /proc/cpuinfo)

# Start slave
cd /slave/$SLAVE
export SLAVE_NAME=${SLAVE_NAME}-${SLAVE_MODE}
mkdir -p $SLAVE_NAME
. ./env &&
twistd -ny /host/scripts/buildbot.tac
echo "Done"
