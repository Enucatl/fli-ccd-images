#!/usr/bin/env python
from __future__ import division, print_function

import os
import argparse
import math

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from th2_to_numpy import th2_to_numpy
import numpy as np
import matplotlib.pyplot as plt

from phase_stepping_utils import average_curve
from phase_stepping_utils import get_signals
from phase_stepping_utils import commandline_parser
from handle_projection_stack import get_projection_stack

commandline_parser.description = __doc__
commandline_parser.add_argument('--flat', metavar='FLAT_FILE(s).root',
        nargs='+',
        help='ROOT file(s) with the histogram for the flat field')
commandline_parser.add_argument('--n_flats', metavar='N_FLATS',
        nargs='?', type=int, default=1,
        help='flats to average (default 1)')
commandline_parser.add_argument('--flats_every', metavar='N_FLATS',
        nargs='?', type=int, default=999999,
        help='flats taken every N_FLATS steps (default 999999)')
commandline_parser.add_argument('--lines', metavar='LINES',
        nargs=1, type=int,
        help='number of lines in the projections (default 1)')


if __name__ == '__main__':
    args = commandline_parser.parse_args()
    root_file, histogram = get_projection_stack(args)
    args.file = args.flat
    flat_root_file, flat_histogram = get_projection_stack(args)
    n_lines = args.lines[0]
    extension = args.format[0]
    roi = args.roi
    n_periods = args.periods
    image_array = th2_to_numpy(histogram)[:,roi[0]:roi[1]]
    flat_image = th2_to_numpy(flat_histogram)[:,roi[0]:roi[1]]
    flat_parameters = get_signals(flat_image, n_periods=n_periods)
    images = np.split(image_array, n_lines, axis=0)
    absorption_image = np.zeros((n_lines, image_array.shape[1]))
    differential_phase_image = np.zeros_like(absorption_image)
    dark_field_image = np.zeros_like(absorption_image)
    for i, phase_stepping_curve in enumerate(images):
        absorption, phase, dark_field = get_signals(
                phase_stepping_curve,
                flat_parameters,
                n_periods)
        absorption_image[i, :] = absorption
        differential_phase_image[i, :] = phase
        dark_field_image[i, :] = dark_field

    f, (ax1, ax2, ax3) = plt.subplots(
            3, 1, sharex=True)
    plt.subplots_adjust(
            left=0.0, right=1.0,
            #bottom=0.0, top=1,
            wspace=0, hspace=0)
    img1 = ax1.imshow(absorption_image, cmap=plt.cm.Greys)
    #ax1.set_title("absorption")
    ax1.axis("off")
    img2 = ax2.imshow(differential_phase_image, cmap=plt.cm.Greys_r)
    img2.set_clim(0, 1.5)
    #ax2.set_title("differential phase")
    ax2.axis("off")
    img3 = ax3.imshow(dark_field_image, cmap=plt.cm.Greys_r)
    #ax3.set_title("dark field")
    img3.set_clim(0, 2)
    ax3.axis("off")
    if absorption_image.shape[0] == 1:
        f, (hist1, hist2, hist3) = plt.subplots(
                3, 1, sharex=True)
        hist1.hist(range(absorption_image.shape[1]),
                bins=absorption_image.shape[1],
                weights=absorption_image.T, fc='w', ec='k')
        hist2.hist(range(differential_phase_image.shape[1]),
                bins=differential_phase_image.shape[1],
                weights=differential_phase_image.T, fc='w', ec='k')
        hist3.hist(range(dark_field_image.shape[1]),
                bins=dark_field_image.shape[1],
                weights=dark_field_image.T, fc='w', ec='k')
    #plt.figure()
    #plt.hist(image_array.flatten(), 256,
            #range=(np.amin(image_array),
                #np.amax(image_array)), fc='w', ec='k')
    #plt.figure()
    #plt.hist(dark_field_image.flatten(), 256,
            #range=(np.amin(dark_field_image),
                #np.amax(dark_field_image)), fc='k', ec='k')
    #plt.figure()
    #plt.hist(differential_phase_image.flatten(), 256,
            #range=(np.amin(differential_phase_image),
                #np.amax(differential_phase_image)), fc='k', ec='k')
    print("mean phase {0:.4f} +- {1:.4f}".format(
            np.mean(differential_phase_image),
            np.std(differential_phase_image) /
            math.sqrt(roi[1] - roi[0])))
    plt.savefig(root_file.GetName().replace(".root",
        "." + extension))
    plt.show()
