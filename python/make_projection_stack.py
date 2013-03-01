#!/usr/bin/env python                                                                                                                                         
from __future__ import division, print_function                                                                                                               
from progress_bar import progress_bar                                                                                                                         
from subprocess import check_call
import os
import argparse

parser = argparse.ArgumentParser(description='''draw a stack of a projection
        along pixel PIXEL of all the images in the ROOT file''')
parser.add_argument('file', metavar='FILE.root',
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
from rootstyle import tdrstyle

tdrstyle()

root_file = ROOT.TFile(root_file_name)
list_of_keys = root_file.GetListOfKeys()
next_item = ROOT.TIter(list_of_keys)
key = next_item.next()
obj = key.ReadObj()
while not obj.InheritsFrom("TH2"):
    key = next_item.next()
    obj = key.ReadObj()

#check pixel command line arg
if len(pixel) == 1:
    pixel.append(pixel[0])
elif len(pixel) > 2:
    print("only two pixels (begin and end) can be specified!")
    raise OSError

pixel = [int(x) for x in pixel]

canvas = ROOT.TCanvas("canvas", "canvas")
canvas.cd()

title = "{0}; x pixel; file number".format(root_file_name)
n_bins_x = obj.GetNbinsX()
n_images = list_of_keys.GetSize()
stack = ROOT.TH2D("stack", title,
        n_bins_x,
        obj.GetXaxis().GetXmin(),
        obj.GetXaxis().GetXmax(),
        n_images,
        0,
        n_images)

for i, key in enumerate(list_of_keys):
    print(progress_bar((i + 1)/n_images), end="")
    name = key.GetName()
    obj = key.ReadObj()
    if not obj.InheritsFrom("TH2"):
        continue
    first_pixel = int(obj.GetYaxis().GetBinLowEdge(1))
    projection = obj.ProjectionX("_px", pixel[0] - first_pixel, pixel[1] -
            first_pixel)
    for j in range(n_bins_x):
        stack.SetBinContent(j + 1, i + 1,
                projection.GetBinContent(j + 1))

stack.Draw()
canvas.SaveAs("stack.png")
print()
print("Done!")
raw_input()
