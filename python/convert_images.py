#!/usr/bin/env python

from __future__ import division, print_function
from progress_bar import progress_bar
from subprocess import check_call
import os
import argparse

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from rootstyle import tdrstyle_grayscale
from iterate_over_histograms import HistogramIterator

parser = argparse.ArgumentParser(description='''convert all images to an image format,
        and save a GIF with imagemagick convert''')
parser.add_argument('file', metavar='FILE.root', 
        nargs=1, help='root file containing the images as TH2D')
parser.add_argument('--format', metavar='FORMAT',
        nargs=1, default="gif", help='format of the images to be stored, default GIF')

args = parser.parse_args()
root_file_name = args.file[0]
extension = args.format[0].lower()


if not os.path.exists(root_file_name):
    print("File not found!", root_file_name)
    print()
    raise OSError

"""Make output folder"""
parent_dir = os.path.dirname(root_file_name)
image_dir = os.path.join(parent_dir, extension)
if not os.path.exists(image_dir):
    os.makedirs(image_dir)

"""open ROOT file"""
root_file = ROOT.TFile(root_file_name)
tdrstyle_grayscale()
iterator = HistogramIterator(root_file)
example_hist = iterator[0]
width = example_hist.GetNbinsX()
height = example_hist.GetNbinsY()
palette = ROOT.gHistImagePalette
n_images = len(iterator)

image = ROOT.TASImage(width, height)
print()
print("drawing images...")
image_file_name = ""
if extension == "gif":
    image_file_name = os.path.basename(
                os.path.normpath(parent_dir))
    image_file_name = os.path.join(image_dir, image_file_name)
    image_file_name += "." + extension
else:
    image_file_name = os.path.join(image_dir, "")

for i, hist in enumerate(iterator):
    print(progress_bar((i + 1) / n_images), end="")
    write_as = image_file_name
    if extension == "gif":
        if i < (n_images - 1):
            write_as += "+3" #+30ms per image
        else:
            write_as += "++1" #1 loop
    else:
        write_as = image_file_name + hist.GetName() + "." + extension
    image.SetImage(hist.GetBuffer(), width, height, palette)
    image.WriteImage(write_as)

if extension == "gif":
    print("created gif file", image_file_name)
else:
    print("created image files in", image_dir)
