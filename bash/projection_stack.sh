#!/usr/bin/env bash
root_file=$(./bash/scan_folder.sh $1).root
echo $root_file
./bash/make_root.sh $1
shift
echo ./python/projection_stack.py $root_file 
./python/projection_stack.py $root_file 
