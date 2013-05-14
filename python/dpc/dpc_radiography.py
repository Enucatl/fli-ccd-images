#!/usr/bin/env python
from __future__ import division, print_function

import os
import argparse
import math

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

import readimages_utils.rcparams
from readimages_utils.hadd import hadd
from dpc.phase_stepping_utils import average_curve
from dpc.phase_stepping_utils import get_signals
from dpc.commandline_parser import commandline_parser
from projections.projection_stack import get_projection_stack

def subtract_drift(image, draw=False):
    """Fit a vertical line to the phase image in order to subtract a
    linear phase drift.

    """
    x = np.arange(image.shape[0])
    y = np.sum(image, axis=1) / image.shape[1]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    line = slope * x + intercept
    correction = np.tile(line,
            (image.shape[1], 1)).transpose()
    corrected_image = image - correction
    if draw:
        plt.figure()
        axis = plt.axes()
        axis.set_title("phase drift interpolation")
        plt.plot(x, line, 'r-', x, y, 'o')
        plt.xlabel('image number')
        plt.ylabel('average phase (rad)')
        #plt.figure()
        #image = plt.imshow(corrected_image)
        #image.set_clim(-0.5, 0.5)
    return corrected_image

class ImageReconstructor(object):
    """Reconstruct the three signals from the phase stepping curve of the
    grating interferometer.
    
    """

    def __init__(self, args):
        self.overwrite = args.overwrite
        image_array = get_projection_stack(args.file, args)
        flat_image = get_projection_stack(args.flat, args)
        self.n_steps = args.steps[0]
        self.n_periods = args.periods
        """Average flats if more than one flat image."""
        self.n_flats = flat_image.shape[0] // self.n_steps
        flat_images = np.split(flat_image, self.n_flats, axis=0)
        flat_absorption = np.zeros((self.n_flats, flat_image.shape[1]))
        flat_phase = np.zeros_like(flat_absorption)
        flat_dark_field = np.zeros_like(flat_absorption)
        for i, phase_stepping_curve in enumerate(flat_images):
            absorption, phase, dark_field = get_signals(
                    phase_stepping_curve,
                    None, self.n_periods)
            flat_absorption[i, :] = absorption
            flat_phase[i, :] = phase
            flat_dark_field[i, :] = dark_field
        print("subtracting drift")
        if self.n_flats > 1:
            corrected_flat_phase = subtract_drift(flat_phase)
        else:
            corrected_flat_phase = flat_phase
        average_absorption = np.mean(flat_absorption, axis=0)
        average_phase = np.mean(corrected_flat_phase, axis=0)
        average_dark_field = np.mean(flat_dark_field, axis=0)
        self.flat_parameters = (average_absorption,
                average_phase,
                average_dark_field)
        self.output_name = hadd(args.file).replace(
                ".hdf5",
                "." + args.format[0])
        self.n_lines = image_array.shape[0] // self.n_steps 
        if image_array.shape[0] % self.n_steps:
            raise ValueError("""
            wrong number of steps,
            division does not result in an integer.
            Image shape: {0}""".format(image_array.shape))
        self.extension = args.format[0]
        self.images = np.split(image_array, self.n_lines, axis=0)
        self.absorption_image = np.zeros((self.n_lines, image_array.shape[1]))
        self.differential_phase_image = np.zeros_like(self.absorption_image)
        self.dark_field_image = np.zeros_like(self.absorption_image)

    def calculate_images(self):
        for i, phase_stepping_curve in enumerate(self.images):
            absorption, phase, dark_field = get_signals(
                    phase_stepping_curve,
                    self.flat_parameters,
                    self.n_periods)
            self.absorption_image[i, :] = absorption
            self.differential_phase_image[i, :] = phase
            self.dark_field_image[i, :] = dark_field
        self.absorption_image_title = "absorption image"
        self.differential_phase_image_title = "differential phase"
        self.dark_field_image_title = "visibility reduction"

    def draw(self):
        f, (ax1, ax2, ax3) = plt.subplots(
                3, 1, sharex=True)
        img1 = ax1.imshow(self.absorption_image,
                cmap=plt.cm.Greys)
        ax1.axis("off")
        ax1.set_title(self.absorption_image_title)
        img2 = ax2.imshow(self.differential_phase_image)
        img2.set_clim(-0.4, 0.4)
        ax2.axis("off")
        ax2.set_title(self.differential_phase_image_title)
        img3 = ax3.imshow(self.dark_field_image)
        ax3.set_title(self.dark_field_image_title)
        ax3.axis("off")
        img3.set_clim(0, 2)
        plt.tight_layout()
        if self.absorption_image.shape[0] == 1:
            f, (hist1, hist2, hist3) = plt.subplots(
                    3, 1, sharex=True)
            hist1.hist(range(self.absorption_image.shape[1]),
                    bins=self.absorption_image.shape[1],
                    weights=self.absorption_image.T, fc='w', ec='k')
            hist1.set_title("absorption")
            hist2.hist(range(self.differential_phase_image.shape[1]),
                    bins=self.differential_phase_image.shape[1],
                    weights=self.differential_phase_image.T, fc='w', ec='k')
            hist2.set_title("differential phase")
            hist3.hist(range(self.dark_field_image.shape[1]),
                    bins=self.dark_field_image.shape[1],
                    weights=self.dark_field_image.T, fc='w', ec='k')
            hist3.set_title("visibility reduction")
        #plt.figure()
        #plt.hist(image_array.flatten(), 256,
                #range=(np.amin(image_array),
                    #np.amax(image_array)), fc='w', ec='k')
        #plt.figure()
        #plt.hist(self.dark_field_image.flatten(), 256,
                #range=(np.amin(self.dark_field_image),
                    #np.amax(self.dark_field_image)), fc='k', ec='k')
        #plt.figure()
        #plt.hist(self.differential_phase_image.flatten(), 256,
                #range=(np.amin(self.differential_phase_image),
                    #np.amax(self.differential_phase_image)), fc='k', ec='k')
        #print("mean phase {0:.4f} +- {1:.4f}".format(
                #np.mean(self.differential_phase_image),
                #np.std(self.differential_phase_image) /
                #math.sqrt(roi[1] - roi[0])))
        if not os.path.exists(self.output_name) or self.overwrite:
            plt.savefig(self.output_name)
            print("saved", self.output_name)
        plt.ion()
        plt.show()
        raw_input("Press ENTER to quit.")

    def correct_drift(self, draw=False):
        self.differential_phase_image_title += " (drift corrected)"
        self.differential_phase_image = subtract_drift(
                self.differential_phase_image, draw)
        
commandline_parser.description = ImageReconstructor.__doc__

if __name__ == '__main__':
    args = commandline_parser.parse_args()
    ir = ImageReconstructor(args)
    ir.calculate_images()
    ir.correct_drift()
    ir.draw()
