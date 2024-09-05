#!/bin/bash

function show_usage {
    echo "Usage: $0 <type>"
    echo "type: The type of the operation (search or rag)"
    exit 1
}


if [[ $# -ne 1 || ! $1 =~ ^(search|rag)$ ]]; then
    show_usage
else
    python main.py $1
    exit 0
fi

