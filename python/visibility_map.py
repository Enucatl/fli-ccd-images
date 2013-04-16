#!/usr/bin/env python
from __future__ import division, print_function

import os

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import numpy as np

from rootstyle import tdrstyle_grayscale
from progress_bar import progress_bar
from base_rootfile_analyser import commandline_parser
from dpc_radiography import get_signals
from th2_to_numpy import th2_to_numpy
from handle_projection_stack import get_projection_stack

commandline_parser.description = __doc__
commandline_parser.add_argument('--periods', metavar='PERIODS',
        type=int, default=1,
        help='number of phase stepping periods')

if __name__ == '__main__':
    tdrstyle_grayscale()
    args = commandline_parser.parse_args()
    roi = args.roi
    n_periods = args.periods
    root_file, histogram = get_projection_stack(args)
    width = histogram.GetNbinsX()
    height = histogram.GetNbinsY()
    visibility_histogram = ROOT.TH1D("visibility",
            "visibility map;pixel;visibility",
            width, 0, width)
    image_array = th2_to_numpy(histogram)
    a0, _, a1 = get_signals(image_array, n_periods=n_periods)
    visibility = 2 * a1 / a0
    for i in range(width):
            visibility_histogram.SetBinContent(i + 1, visibility[i])
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
