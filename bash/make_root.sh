#!/usr/bin/env bash
echo "making root file from folder"
folder=$(./bash/scan_folder.sh $1)
echo $folder
./bin/make_root $folder
