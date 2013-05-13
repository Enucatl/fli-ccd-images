#!/usr/bin/env bash
set -vx
n=$1
folder=$(./bash/scan_folder.sh $n)
hdf5_file=$(folder).hdf5
if [ ! -f $(hdf5_file) ]
then
    ./bash/make_hdf5.sh $n
fi
shift
intensity_scan.py $folder.hdf5 --roi "$*"
