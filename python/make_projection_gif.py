#!/usr/bin/env python                                                                                                                                         
from __future__ import division, print_function                                                                                                               
from progress_bar import progress_bar                                                                                                                         
from subprocess import check_call
import os
import argparse
parser = argparse.ArgumentParser(description='''save GIF with projection
        along pixel PIXEL''')
parser.add_argument('file', metavar='FILE',
        nargs=1, help='ROOT file with the RAW images converted to TH2D')
parser.add_argument('pixel', metavar='PIXELS',
        nargs='+', help='pixel number(s)')

root_file_name = parser.parse_args().file[0]
pixel = parser.parse_args().pixel

#setup program name:
if not os.path.exists(root_file_name):
    print("File not found!", root_file_name)
    print()
    raise OSError


import ROOT

root_file = ROOT.TFile(root_file_name)
list_of_keys = root_file.GetListOfKeys()
next_item = ROOT.TIter(list_of_keys)
key = next_item.next()

canvas = ROOT.TCanvas("canvas", "canvas")

#check pixel command line arg
if len(pixel) == 1:
    pixel.append(pixel[0])
elif len(pixel) > 2:
    print("only two pixels (begin and end) can be specified!")
    raise OSError

pixel = [int(x) for x in pixel]


while key:
    print(key.GetName())
    obj = key.ReadObj()
    projection = obj.ProjectionX("projection", pixel[0], pixel[1])
    projection.Draw()
    print(projection.Integral(), obj.Integral())
    try:
        key = next_item.next()
    except StopIteration:
        break
