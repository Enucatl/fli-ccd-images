#!/usr/bin/env bash
echo "making root file from folder"
echo "$(./bash/scan_folder.sh $1)"
./bin/make_root $(./bash/scan_folder.sh $1)
