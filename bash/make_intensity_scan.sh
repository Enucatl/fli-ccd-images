#!/usr/bin/env bash
n=$1
folder=/afs/psi.ch/project/hedpc/raw_data/2013/ccdfli/2013.03.21/S00000-00999/
./bin/make_root $folder/S000$n
python python/intensity_scan.py $folder/S000$n.root --roi $2 $3 $4 $5
