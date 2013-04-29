#!/usr/bin/env bash
set -vx
n=$1
root_file=$(./bash/scan_folder.sh $1).root
if [ ! -f $(root_file) ]
then
    ./bash/make_root.sh $1
fi
shift
export_images.py $root_file --format tif "$*"
