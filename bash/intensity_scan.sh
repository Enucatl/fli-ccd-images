#!/usr/bin/env bash
n=$1
folder=$(./bash/scan_folder.sh $n)
./bash/make_root.sh $n
shift
python python/intensity_scan.py $folder.root --roi "$*"
