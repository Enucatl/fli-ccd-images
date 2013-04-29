#!/usr/bin/env bash
set -vx
root_file=$(./bash/scan_folder.sh $1).root
if [ ! -f $(root_file) ]
then
    ./bash/make_root.sh $1
fi
shift
projection_stack.py $root_file 
