#!/usr/bin/env python
# encoding: utf-8

from __future__ import division, print_function

"""Get a list of files, return a plot of the phase drift in each pixel."""

import matplotlib.pyplot as plt
import math
import numpy as np

from projections.handle_projection_stack import get_projection_stack
from readimages_utils.th2_to_numpy import th2_to_numpy
from dpc.commandline_parser import commandline_parser
from dpc.phase_stepping_utils import get_signals

if __name__ == '__main__':
    args = commandline_parser.parse_args()
    roi = args.roi
    n_lines = args.lines[0]
    n_intervals = n_lines - 1
    phase_drift = np.zeros((n_intervals, roi[1] - roi[0]))
    root_file, histogram = get_projection_stack(args)
    image_array = th2_to_numpy(histogram)[:,roi[0]:roi[1]]
    images = np.split(image_array, n_lines, axis=0)
    n_periods = args.periods
    for i, (first_array, second_array) in enumerate(zip(images, images[1:])):
        flat_pars = get_signals(first_array, n_periods=args.periods)
        _, phi, _ = get_signals(second_array, flat_pars, n_periods=args.periods)
        phase_drift[i, :] = phi
    mean_drift_array = np.mean(phase_drift, axis=0)
    std_dev = np.std(phase_drift, axis=0) / math.sqrt(n_intervals)
    plt.figure()
    plt.errorbar(range(roi[0], roi[1]), mean_drift_array, yerr=std_dev, fmt='ro')
    mean_drift = (np.average(mean_drift_array, weights=np.power(std_dev, -2)),
            np.std(mean_drift_array) / math.sqrt(roi[1] - roi[0]))
    print("weighted drift = {0[0]:.5f} +- {0[1]:.5f}".format(mean_drift))
    across_pixels = np.mean(phase_drift, axis=1)
    across_pixels_err = np.std(phase_drift, axis=1) / math.sqrt(roi[1] -
            roi[0])
    plt.figure()
    plt.errorbar(range(n_intervals), across_pixels, yerr=across_pixels_err,
            fmt='ro')
    print("average std dev", np.mean(across_pixels_err) * math.sqrt(roi[1] -
        roi[0]))
    plt.show()
