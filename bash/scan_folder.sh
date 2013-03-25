#!/usr/bin/env bash
echo "/afs/psi.ch/project/hedpc/raw_data/$(date +%Y)/ccdfli/$(date +%Y.%m.%d)/S00000-00999/S$(printf "%05d" $1)"
