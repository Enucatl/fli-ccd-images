#!/usr/bin/env bash
set -vx
n=$1
hdf5_file=$(./bash/scan_folder.sh $1).hdf5
if [ ! -f $(hdf5_file) ]
then
    ./bash/make_hdf5.sh $1
fi
shift
export_images.py $hdf5_file --format tif "$*"
