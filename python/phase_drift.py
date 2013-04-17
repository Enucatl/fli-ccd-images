#!/usr/bin/env python
# encoding: utf-8

from __future__ import division, print_function

"""Get a list of files, return a plot of the phase drift in each pixel."""

import ROOT
import numpy as np

from th2_to_numpy import th2_to_numpy
from dpc_radiography import commandline_parser
from handle_projection_stack import get_projection_stack
from phase_stepping_utils import get_signals
from rootstyle import tdrstyle_grayscale

if __name__ == '__main__':
    args = commandline_parser.parse_args()
    roi = args.roi
    n_lines = args.lines[0]
    n_intervals = n_lines - 1
    phase_drift_histogram = ROOT.TH2D("phase_drift",
            "phase drift; pixel; file number",
            roi[1] - roi[0], roi[0], roi[1],
            n_intervals, 0, n_intervals)

    root_file, histogram = get_projection_stack(args)
    image_array = th2_to_numpy(histogram)[:,roi[0]:roi[1]]
    images = np.split(image_array, n_lines, axis=0)
    n_periods = args.periods
    for i, (first_array, second_array) in enumerate(zip(images, images[1:])):
        flat_pars = get_signals(first_array, n_periods=args.periods)
        _, phi, _ = get_signals(second_array, flat_pars, n_periods=args.periods)
        for j, phase_difference in enumerate(phi):
            phase_drift_histogram.SetBinContent(
                    j + 1, i + 1, phase_difference)
    drift_histogram_canvas = ROOT.TCanvas("drift_histogram_canvas", "drift_histogram_canvas")
    phase_drift_histogram.Draw("col")
    profile_canvas = ROOT.TCanvas("profile_canvas", "profile_canvas")
    profile = phase_drift_histogram.ProfileX()
    profile.Draw()
    profile_canvas.Update()
    raw_input()
