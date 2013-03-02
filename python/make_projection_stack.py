#!/usr/bin/env python

from __future__ import division, print_function
import os
import argparse
from subprocess import check_call

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from progress_bar import progress_bar
from rootstyle import tdrstyle_grayscale
from iterate_over_histograms import HistogramIterator

tdrstyle_grayscale()

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

root_file = ROOT.TFile(root_file_name, "update")
root_file.cd()
"""make subdir if it doesn't exist"""
dir_name = "postprocessing"
directory = root_file.Get(dir_name)
if not directory:
    directory = root_file.mkdir("postprocessing")
directory.cd()
iterator = HistogramIterator(root_file)

#check pixel command line arg
if len(pixel) == 1:
    pixel.append(pixel[0])
elif len(pixel) > 2:
    print("only two pixels (begin and end) can be specified!")
    raise OSError

canvas = ROOT.TCanvas("canvas", "canvas")

title = "{0} along pixel {1[0]}-{1[1]}; x pixel; file number".format(
        root_file_name,
        pixel)
hist = iterator[0]
n_bins_x = hist.GetNbinsX()
n_images = len(iterator)
stack = ROOT.TH2D("stack_pixel_{0[0]}_{0[1]}".format(
    pixel), title,
        n_bins_x,
        hist.GetXaxis().GetXmin(),
        hist.GetXaxis().GetXmax(),
        n_images,
        0,
        n_images)

pixel = [int(x) for x in pixel]
print()
print("drawing stack...")
for i, hist in enumerate(iterator):
    print(progress_bar((i + 1)/n_images), end="")
    name = hist.GetName()
    if not hist.InheritsFrom("TH2"):
        continue
    first_pixel = int(hist.GetYaxis().GetBinLowEdge(1))
    projection = hist.ProjectionX("_px", pixel[0] - first_pixel, pixel[1] -
            first_pixel)
    for j in range(n_bins_x):
        stack.SetBinContent(j + 1, i + 1,
                projection.GetBinContent(j + 1))

print()
stack.Draw("col")
stack.Write()
canvas.Update()
print()
print("Done!")
print()
raw_input()
