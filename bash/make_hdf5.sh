#!/usr/bin/env bash
set -vx
folder=$(./bash/scan_folder.sh $1)
./bin/make_hdf5 $folder
