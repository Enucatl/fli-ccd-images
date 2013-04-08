#!/usr/bin/env bash
echo "projection stack on pixel 515 from file"
root_file=$(./bash/scan_folder.sh $1).root
echo $root_file
./bash/make_root.sh $1
./python/projection_stack.py $root_file 508
