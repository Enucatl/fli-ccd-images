#!/usr/bin/env python
"""Draw the graph of the visibility in each pixel.

If more than one phase stepping curve is found in the file,
the output is the average visibility for each phase stepping curve.

"""

from __future__ import division, print_function

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from dpc.commandline_parser import commandline_parser
from dpc.dpc_radiography import get_signals
from projections.projection_stack import get_projection_stack

commandline_parser.description = __doc__

if __name__ == '__main__':
    args = commandline_parser.parse_args()
    roi = args.roi
    n_periods = args.periods
    image_array = get_projection_stack(args.file, args)
    n_steps = args.steps[0]
    n_images = image_array.shape[0] // n_steps
    if image_array.shape[0] % n_steps:
        raise ValueError("incorrect number of steps! {0}".format(
            image_array.shape))
    image = np.dstack(np.split(image_array, n_images, axis=0))
    image = np.rollaxis(image, 2, 1)
    a0, _, a1 = get_signals(image, n_periods=n_periods)
    visibility = (2 * a1 / a0)
    mean_visibility = np.mean(visibility, axis=1)
    std_dev_visibility = np.std(visibility, axis=1) / visibility.shape[1]
    plt.figure()
    axis = plt.axes()
    if visibility.shape[0] == 1:
        plt.plot(np.arange(roi[0], roi[1]), visibility.T)
        plt.xlim(roi[0], roi[1])
        plt.xlabel("pixel number")
        plt.ylabel("visibility $2 a_1 / a_0$ ($\\%$)")
        mean_visibility = mean_visibility[0]
        line = plt.axhline(y=mean_visibility, color='r')
        plt.legend([line], ["average visibility: {0:.2f} $\\%$".format(
            mean_visibility * 100)])
    else:
        plt.errorbar(
                np.arange(1, mean_visibility.shape[0] + 1),
                mean_visibility,
                yerr=std_dev_visibility,
                fmt='o'
                )
        plt.xlim(0, mean_visibility.shape[0] + 1)
        plt.xlabel("image number")
        plt.ylabel("average visibility $2 a_1 / a_0$ ($\\%$)",
                )
    axis.yaxis.set_major_formatter(FuncFormatter(
        lambda x, pos=0: "{0:.2%}".format(x)))
    plt.tight_layout()
    plt.ion()
    plt.show()
    raw_input("Press ENTER to quit.")
