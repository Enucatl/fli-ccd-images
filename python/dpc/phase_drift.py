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
    root_file, histogram = get_projection_stack(args)
    image_array = th2_to_numpy(histogram, roi)
    n_steps = args.steps[0]
    n_lines = image_array.shape[0] // n_steps 
    n_periods = args.periods
    n_intervals = n_lines - 1
    n_pixels = image_array.shape[1]
    images = np.split(image_array, n_lines, axis=0)
    phase_drift = np.zeros((n_intervals, n_pixels))
    for i, (first_array, second_array) in enumerate(zip(images, images[1:])):
        flat_pars = get_signals(first_array, n_periods=n_periods)
        _, phi, _ = get_signals(second_array, flat_pars, n_periods=n_periods)
        phase_drift[i, :] = phi
    mean_drift_array = np.mean(phase_drift, axis=0)
    std_dev = np.std(phase_drift, axis=0) / math.sqrt(n_intervals - 1)
    across_steps_figure = plt.figure()
    #ax1 = plt.axes((0.18, 0.20, 0.55, 0.65))
    ax1 = plt.axes()
    ax1.set_xlim((roi[0], roi[1]))
    #ax1.spines['top'].set_visible(False)
    #ax1.spines['right'].set_visible(False)
    x_positions = range(roi[0], roi[1])
    plt.plot(x_positions,
            mean_drift_array,
            #yerr=std_dev,
            #fmt='ko',
            clip_on=False,
            )
    plt.xlabel('pixel')
    plt.ylabel('average drift per scan')
    plt.fill_between(x_positions,
            mean_drift_array + std_dev, mean_drift_array - std_dev,
            alpha=0.5,
            facecolor='#089FFF',
            edgecolor='#1B2ACC',
            antialiased=True,
            )
    mean_drift = (np.average(mean_drift_array, weights=np.power(std_dev, -2)),
            np.std(mean_drift_array) / math.sqrt(n_pixels - 1))
    mean_drift_text = "average drift = {0[0]:+.5f} $\\pm$ {0[1]:.5f} rad/scan".format(mean_drift)
    plt.text(350, 0.15, mean_drift_text,
                   fontsize=30,
                   transform=ax1.transData, clip_on=False,
                   va='top', ha='left')
    plt.axhline(color='r')
    plt.savefig("pixels.png")
    """Now across pixels"""
    across_pixels_figure = plt.figure()
    across_pixels = np.mean(phase_drift, axis=1)
    across_pixels_err = (np.std(phase_drift, axis=1) /
            math.sqrt(n_pixels - 1))
    plt.errorbar(range(n_intervals),
            across_pixels,
            yerr=across_pixels_err,
            fmt='bo'
        )
    plt.xlabel('scan')
    plt.ylabel('average drift')
    print("average std dev", np.mean(across_pixels_err) * math.sqrt(
        n_pixels - 1))
    plt.axhline(color='r')
    plt.show()
