#!/usr/bin/env bash
set -vx
n=$1
folder=$(./bash/scan_folder.sh $n)
if [ ! -f $(root_file) ]
then
    ./bash/make_root.sh $n
fi
shift
intensity_scan.py $folder.root --roi "$*"
