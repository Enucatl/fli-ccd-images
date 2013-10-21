#!/usr/bin/env python
"""Draw the graph of the visibility in each pixel.

If more than one phase stepping curve is found in the file,
the output is the average visibility for each phase stepping curve.

"""

from __future__ import division, print_function

import numpy as np
import h5py
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from readimages.dpc.commandline_parser import commandline_parser
from readimages.dpc.phase_stepping_utils import get_signals
from readimages.projections.get_projection_stack import get_projection_stack
from readimages.utils.hadd import hadd

commandline_parser.description = __doc__

if __name__ == '__main__':
    import pkg_resources
    version = pkg_resources.require("readimages")[0].version
    print("\n", commandline_parser.prog, version, end="\n\n")

    args = commandline_parser.parse_args()
    roi = args.roi
    n_periods = args.periods
    image_array = get_projection_stack(
            args.file, args.pixel,
            args.roi, args.overwrite)
    n_steps = args.steps
    n_images = image_array.shape[0] // n_steps
    if image_array.shape[0] % n_steps:
        raise ValueError("incorrect number of steps! {0}".format(
            image_array.shape))
    image = np.dstack(np.split(image_array, n_images, axis=0))
    image = np.rollaxis(image, 2, 1)
    a0, _, a1 = get_signals(image, n_periods=n_periods)
    visibility = (2 * a1 / a0)
    pixels = np.arange(roi[0], roi[1])
    mean_visibility = np.mean(visibility, axis=1)
    std_dev_visibility = np.std(visibility, axis=1) / visibility.shape[1]
    plt.figure()
    axis = plt.axes()
    if visibility.shape[0] == 1:
        plt.plot(pixels, visibility.T)
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
        plt.ylabel("average visibility $2 a_1 / a_0$ ($\\%$)")
    axis.yaxis.set_major_formatter(FuncFormatter(
        lambda x, pos=0: "{0:.2%}".format(x)))
    plt.tight_layout()
    if not args.batch:
        plt.ion()
        plt.show()
        raw_input("Press ENTER to quit.")

    """Save to hdf5 file"""
    output_object = np.vstack((pixels, visibility))
    output_name = "postprocessing/visibility_{0}".format(args.pixel)
    output_file_name = hadd(args.file)
    output_file = h5py.File(output_file_name)
    if output_name in output_file:
        del output_file[output_name]
    output_file.create_dataset(output_name, data=output_object)
    print("Saved", os.path.join(output_file_name, output_name))
