#!/usr/bin/env bash
echo "projection stack on pixel 515 from file"
root_file=$(./bash/scan_folder.sh $1).root
echo $root_file
./python/projection_stack.py $root_file 515
