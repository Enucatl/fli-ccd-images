#!/usr/bin/env python
# encoding: utf-8

from __future__ import division, print_function

"""Get a list of files, return a plot of the phase drift in each pixel."""

import matplotlib.pyplot as plt
import math
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
    mean_drift = (np.mean(mean_drift_array),
            np.std(mean_drift_array) / math.sqrt(roi[1] - roi[0]))
    print("mean drift = {0[0]:.5f} +- {0[1]:.5f}".format(mean_drift))
    plt.show()
