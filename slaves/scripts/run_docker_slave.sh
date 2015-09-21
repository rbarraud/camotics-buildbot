#!/bin/bash

CMD="$0"
ARGS=$*

SLAVE_CMD=
SLAVE_BUILD=false
SLAVE_FG=false
SLAVE_TEST=false
SLAVE_MODE=release

usage() {
    echo "Usage: $CMD [OPTIONS]"
    echo "  -n <name>            Set the slave name"
    echo "  -p <pass>            Set the slave password"
    echo "  -m <debug|release>   Set the slave mode"
    echo "  -c <cmd>             Execute docker command on running slave"
    echo "  -f                   Run the slave in the foreground"
    echo "  -s                   Stop the slave"
    echo "  -t                   Test build results"
    echo "  -b                   Build but do not run the slave"
    echo "  -h|--help            Print this screen and exit"

    if [ "$1" != "" ]; then
        echo
        echo "ERROR: $1"
        exit 1
    fi

    exit 0
}


is_running() {
    docker top $1 2>/dev/null >/dev/null
    return $?
}


container_exists() {
    docker inspect $1 2>/dev/null >/dev/null
    return $?
}


while [ ${#} -gt 0 ]; do
    case $1 in
        -n) SLAVE_NAME="$2"; shift ;;
        -p) SLAVE_PASS="$2"; shift ;;
        -m) SLAVE_MODE="$2"; shift ;;
        -c) SLAVE_CMD="$2"; shift ;;
        -f) SLAVE_FG=true ;;
        -s) SLAVE_CMD=stop ;;
        -t) SLAVE_TEST=true ;;
        -b) SLAVE_BUILD=true ;;
        -h|--help) usage ;;
    esac

    shift
done

if [ "$SLAVE_NAME" == "" ]; then usage "SLAVE_NAME not set"; fi

SCRIPTS="$(dirname "$0")"
TAG=camotics-$(echo "$SLAVE_NAME" | sed 's/\(.*\)/\L\1/;s/[^a-zA-Z0-9_-]//g')
SLAVE_DIR=$SLAVE_NAME

if $SLAVE_TEST; then
    SLAVE_DIR=${SLAVE_DIR}/test
    TAG=${TAG}-test
    SLAVE_FG=true
fi

SLAVE_ID=${TAG}-${SLAVE_MODE}

cd "$SCRIPTS"/..

if [ "$SLAVE_CMD" != "" ]; then
    if ! container_exists $SLAVE_ID; then
        echo "Container $SLAVE_ID does not exist"
        exit 1
    fi

    CMD="docker $SLAVE_CMD $SLAVE_ID"
    echo $CMD
    $CMD
    RET=$?
    exit $RET
fi

if is_running $SLAVE_ID; then
    echo "Slave ${SLAVE_ID} appears to be already running"
    exit 1
fi

# Make sure it's built
if (! container_exists $SLAVE_ID) || $SLAVE_BUILD; then
    docker build --rm -t $TAG $SLAVE_DIR || exit 1
fi


if ! $SLAVE_BUILD; then
    if container_exists $SLAVE_ID; then
        CMD="docker start $SLAVE_ID"

    else
        CMD="docker run --name $SLAVE_ID"

        if $SLAVE_FG; then CMD+=" -it --rm";
        else CMD+=" -d"; fi

        if $SLAVE_TEST; then
            CMD+=" -e DISPLAY"
            CMD+=" -v $HOME/.Xauthority:/home/buildbot/.Xauthority"
            CMD+=" --net=host"
            CMD+=" $TAG"

        else
            if [ "$SLAVE_PASS" == "" ]; then
                echo "SLAVE_PASS not set"
                exit 1
            fi

            CMD+=" -v $PWD:/host"
            CMD+=" $TAG /host/scripts/bootstrap_slave.sh $ARGS"
        fi
    fi

    echo $CMD
    $CMD
fi
