#!/usr/bin/env python
from __future__ import division, print_function

import os

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
from base_rootfile_analyser import commandline_parser
from handle_projection_stack import get_projection_stack

commandline_parser.description = __doc__

if __name__ == '__main__':
    tdrstyle_grayscale()
    args = commandline_parser.parse_args()
    roi = args.roi
    root_file, histogram = get_projection_stack(args)
    width = histogram.GetNbinsX()
    height = histogram.GetNbinsY()
    visibility_histogram = ROOT.TH1D("visibility",
            "visibility map;pixel;visibility",
            width, 0, width)
    for i in range(width):
        projection = histogram.ProjectionY(
                "projectiony_{0}".format(i + 1),
                i + 1, i + 1, "e")
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
        visibility = (maximum - minimum) / (minimum + maximum)
        visibility_histogram.SetBinContent(i + 1, visibility)
    visibility_canvas = ROOT.TCanvas("visibility_canvas",
            "visibility_canvas")
    visibility_histogram.Draw()
    visibility_array = np.fromiter(
            (visibility_histogram.GetBinContent(i + 1)
                for i in range(width)),
        dtype=np.float64)[roi[0]:roi[1]] 
    mean_visibility = np.mean(visibility_array)
    text = ROOT.TPaveText(0.7, 0.94, 0.98, 0.98, "blNDC")
    text.SetFillColor(0)
    text.AddText("mean visibility {0[0]}-{0[1]}: {1:.2%}".format(
        roi, mean_visibility))
    text.Draw()
    visibility_canvas.Update()
    raw_input()
