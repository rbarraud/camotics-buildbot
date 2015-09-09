#!/bin/bash

CMD="$0"
ARGS=$*

SLAVE_CMD=
SLAVE_BUILD=false
SLAVE_FG=false

usage() {
    echo "Usage: $CMD [OPTIONS]"
    echo "  -n <name>            Set the slave name"
    echo "  -p <pass>            Set the slave password"
    echo "  -m <debug|release>   Set the slave mode"
    echo "  -c <cmd>             Execute docker command on running slave"
    echo "  -f                   Run the slave in the foreground"
    echo "  -s                   Stop the slave"
    echo "  -b                   Build but do not run the slave"
    echo "  -h|--help            Print this screen and exit"

    if [ "$1" != "" ]; then
        echo
        echo "ERROR: $1"
        exit 1
    fi

    exit 0
}

while [ ${#} -gt 0 ]; do
    case $1 in
        -n) SLAVE_NAME="$2"; shift ;;
        -p) SLAVE_PASS="$2"; shift ;;
        -m) SLAVE_MODE="$2"; shift ;;
        -c) SLAVE_CMD="$2"; shift ;;
        -f) SLAVE_FG=true ;;
        -s) SLAVE_CMD="stop" ;;
        -b) SLAVE_BUILD=true ;;
        -h|--help) usage ;;
    esac

    shift
done

if [ "$SLAVE_NAME" == "" ]; then usage "SLAVE_NAME not set"; fi
if [ "$SLAVE_MODE" == "" ]; then usage "SLAVE_MODE not set"; fi

SCRIPTS="$(dirname "$0")"
SLAVE="$SLAVE_NAME/$SLAVE_MODE"
TAG=camotics-$(echo "$SLAVE_NAME" | sed 's/\(.*\)/\L\1/;s/[^a-zA-Z0-9_-]//g')
SLAVE_ID=${TAG}-${SLAVE_MODE}.id

cd "$SCRIPTS"/..

if [ "$SLAVE_CMD" != "" ]; then
    if [ ! -e $SLAVE_ID ]; then
        echo "Slave ${SLAVE} does not appear to be running"
        exit 1
    fi

    docker $SLAVE_CMD $(cat $SLAVE_ID)
    RET=$?

    docker top $(cat $SLAVE_ID) 2>/dev/null >/dev/null
    if [ $? -ne 0 ]; then
        echo "Container ended"
        rm $SLAVE_ID
    fi

    exit $RET
fi

if [ -e $SLAVE_ID ]; then
    echo "Slave ${SLAVE} appears to be already running as $(cat $SLAVE_ID)"
    exit 1
fi

docker build --rm -t $TAG $SLAVE_NAME || exit 1

if ! $SLAVE_BUILD; then
    if [ "$SLAVE_PASS" == "" ]; then echo "SLAVE_PASS not set"; exit 1; fi

    CMD="docker run -v $PWD:/host"

    if $SLAVE_FG; then CMD+=" -it";
    else CMD+=" -d"; fi

    CMD+=" $TAG /host/scripts/bootstrap_slave.sh $ARGS"

    echo $CMD

    if $SLAVE_FG; then
        $CMD
    else
        $CMD > $SLAVE_ID
    fi
fi
