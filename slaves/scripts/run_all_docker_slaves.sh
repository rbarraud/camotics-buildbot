#!/bin/bash


usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "  -p <pass>            Set the slave password"
    echo "  -c <cmd>             Execute docker command on slaves"
    echo "  -s                   Stop the slaves"
    echo "  -b                   Build but do not run slaves"
    echo "  -h|--help            Print this screen and exit"

    if [ "$1" != "" ]; then
        echo
        echo "ERROR: $1"
        exit 1
    fi

    exit 0
}


CMD="$(dirname "$0")/run_docker_slave.sh"

while [ ${#} -gt 0 ]; do
    case $1 in
        -p) CMD="$CMD -p $2"; shift ;;
        -c) CMD="$CMD -c $2"; shift ;;
        -s) CMD="$CMD -s" ;;
        -b) CMD="$CMD -b" ;;
        -h|--help) usage ;;
    esac

    shift
done


for MODE in debug release; do
    $CMD -n Debian-Testing-64bit -m $MODE
    $CMD -n Debian-Testing-32bit -m $MODE
    $CMD -n Ubuntu-Precise-64bit -m $MODE
done
