#!/bin/bash
function show_usage {
  echo "Usage: ./script.sh --type=<search|rag>"
  echo "  --type: The type of operation (search or rag)"
  exit 1
}

if [ $# -ne 1 || ! $1 =~ ^(search|rag)$ ]; then
  echo "Usage: ./script.sh (search|rag)"
  exit 1
fi

