#!/usr/bin/env bash
set -vx
folder=$(./bash/scan_folder.sh $1)
make_hdf5.py $folder
