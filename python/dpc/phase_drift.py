#!/usr/bin/env python
# encoding: utf-8

"""Get a list of files, return a plot of the phase drift in each pixel."""

from __future__ import division, print_function

import matplotlib.pyplot as plt
import math
import numpy as np

from projections.projection_stack import get_projection_stack
from dpc.commandline_parser import commandline_parser
from dpc.phase_stepping_utils import get_signals

if __name__ == '__main__':
    args = commandline_parser.parse_args()
    roi = args.roi
    image_array = get_projection_stack(args.file, args)
    n_steps = args.steps[0]
    n_lines = image_array.shape[0] // n_steps 
    n_periods = args.periods
    n_intervals = n_lines - 1
    n_pixels = image_array.shape[1]
    images = np.split(image_array, n_lines, axis=0)
    phase_drift = np.zeros((n_intervals, n_pixels))
    for i, (first_array, second_array) in enumerate(zip(images, images[1:])):
        first = np.dstack(np.split(first_array, 1, axis=0))
        second = np.dstack(np.split(second_array, 1, axis=0))
        flat_pars = get_signals(first, n_periods=n_periods)
        _, phi, _ = get_signals(second, flat_pars, n_periods=n_periods)
        phase_drift[i, :] = phi.transpose()
    mean_drift_array = np.mean(phase_drift, axis=0)
    std_dev = np.std(phase_drift, axis=0) / math.sqrt(n_intervals - 1)
    across_steps_figure = plt.figure()
    ax1 = plt.axes()
    ax1.set_xlim((roi[0], roi[1]))
    x_positions = range(roi[0], roi[1])
    plt.plot(x_positions,
            mean_drift_array,
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
    #plt.savefig("pixels.png")
    #Now across pixels"""
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
    plt.ion()
    plt.show()
    if not args.batch:
        raw_input("Press ENTER to quit.")
