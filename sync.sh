#!/bin/bash -ex

cmd="mpremote"
if ! command -v "$cmd" &> /dev/null; then
    echo "Error: Required utility '$cmd' not found in PATH or not executable"
   exit 1
fi

rm -rf lib/__pycache__
mpremote cp -r boot.py config.py main.py lib : + reset