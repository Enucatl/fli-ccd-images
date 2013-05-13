#!/usr/bin/env python
from __future__ import division, print_function

import os

import numpy as np
import matplotlib.pyplot as plt

from dpc.commandline_parser import commandline_parser
from dpc.dpc_radiography import get_signals
from projections.projection_stack import get_projection_stack

commandline_parser.description = __doc__

if __name__ == '__main__':
    args = commandline_parser.parse_args()
    roi = args.roi
    n_periods = args.periods
    image_array = get_projection_stack(args.file, args)
    a0, _, a1 = get_signals(image_array, n_periods=n_periods)
    visibility = 2 * a1 / a0
    mean_visibility = np.mean(visibility)
    plt.figure()
    plt.plot(np.arange(*roi), visibility,
            antialiased=True)
    plt.xlabel("pixel number")
    plt.ylabel("visibility")
    line = plt.axhline(y=mean_visibility, color='r')
    plt.tight_layout()
    plt.legend([line], ["average visibility: {0:.2f} $\\%$".format(
        mean_visibility * 100)])
    plt.ion()
    plt.show()
    raw_input("Press ENTER to quit.")
