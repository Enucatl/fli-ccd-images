#!/usr/bin/env python
from __future__ import division, print_function

import os
import argparse

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import math
from itertools import islice
from rootstyle import tdrstyle_grayscale
import numpy as np
from scipy import ndimage
from scipy import stats
from skimage import io
from skimage import filter
from skimage import transform
from skimage import morphology
from skimage import img_as_uint
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from rootstyle import tdrstyle_grayscale
from progress_bar import progress_bar

commandline_parser = argparse.ArgumentParser(description='''
        Convert object to image.''')
commandline_parser.add_argument('file', metavar='FILE.root',
        nargs=1, help='ROOT file with the histogram')
commandline_parser.add_argument('--object', metavar='OBJECT',
        nargs=1, default=["postprocessing/stack_pixel_508_508"],
        help='name of the histogram')
commandline_parser.add_argument('--format', metavar='FORMAT',
        nargs=1, default=["tif"], help='output format (default 16bit tif)')

if __name__ == '__main__':
    tdrstyle_grayscale()
    args = commandline_parser.parse_args()
    root_file_name = args.file[0]
    object_name = args.object[0]
    extension = args.format[0]
    root_file = ROOT.TFile(root_file_name, "update")
    if not root_file.IsOpen():
        raise IOError("Could not open {0}.".format(
            root_file_name))
    histogram = root_file.Get(object_name)
    if not histogram:
        raise IOError("Object {0} not found.".format(
            object_name))
    width = histogram.GetNbinsX()
    height = histogram.GetNbinsY()
    visibility_histogram = ROOT.TH1D("visibility",
            "visibility map;pixel;visibility",
            width, 0, width)
    for i in range(width):
        projection = histogram.ProjectionY(
                "projectiony_{0}".format(i + 1),
                i + 1, i + 1, "e")
        transform = projection.FFT(0, "mag r2c ex")
        n_bins = height 
        frequencies = np.fromiter(
                (projection.GetBinContent(i + 1)
                    for i in range(height)),
                dtype=np.uint16)
        mean = np.mean(frequencies)
        std_dev = np.std(frequencies)
        frequencies = np.ma.masked_greater(frequencies,
                mean + 3 * std_dev)
        minimum, median, maximum = stats.mstats.mquantiles(
                frequencies,
                prob=[0, 0.5, 1])
        visibility = (maximum - minimum) / (2 * median)
        visibility_histogram.SetBinContent(i + 1, visibility)
    visibility_canvas = ROOT.TCanvas("visibility_canvas",
            "visibility_canvas")
    visibility_histogram.Draw()
    visibility_array = np.fromiter(
            (visibility_histogram.GetBinContent(i + 1)
                for i in range(width)),
        dtype=np.float64)[200:800] 
    mean_visibility = np.mean(visibility_array)
    text = ROOT.TPaveText(0.7, 0.94, 0.98, 0.98, "blNDC")
    text.SetFillColor(0)
    text.AddText("mean visibility {0:.2%}".format(mean_visibility))
    text.Draw()
    visibility_canvas.Update()
    #median_visibility = np.median(visibility_array)
    #print("median visibility {0:.2%}".format(mean_visibility))
    #image_canvas = ROOT.TCanvas("image_canvas",
            #"image_canvas")
    #histogram.Draw("col")
    raw_input()
