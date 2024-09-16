#!/bin/bash

function show_usage {
    echo "usage: $0 [-h] --verbose | --no-verbose"
    echo "run either ($0 --verbose) or ($0 --no-verbose)"

    exit 1
}


if [[ $# -ne 1 || ! $1 =~ ^(--verbose|--no-verbose)$ ]]; then
    show_usage
else
    python main.py $1
    exit 0
fi

