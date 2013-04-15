#!/usr/bin/env python
from __future__ import division, print_function

import os
import argparse

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import math
from scipy import stats
from th2_to_numpy import th2_to_numpy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

commandline_parser = argparse.ArgumentParser(description='''
        Convert object to image.''')
commandline_parser.add_argument('file', metavar='FILE.root',
        nargs=1, help='ROOT file with the histogram')
commandline_parser.add_argument('--flat', metavar='FLAT_FILE.root',
        nargs=1, help='ROOT file with the histogram for the flat field')
commandline_parser.add_argument('--lines', metavar='LINES',
        nargs=1, type=int, help='number of lines in the projections')
commandline_parser.add_argument('--pixel_file', metavar='INI_FILE',
        nargs=1, default=["data/default_pixel.ini"],
        help='file containing the default pixel height')
commandline_parser.add_argument('--format', metavar='FORMAT',
        nargs=1, default=["tif"], help='output format (default 16bit tif)')
commandline_parser.add_argument('--roi', metavar='FORMAT',
        nargs=2, default=[300, 800], help='region of interest')

def get_signals(phase_stepping_curve, flat=None, n_periods=1):
    """Get the three images from the phase stepping curves.
    flat contains a0, phi and a1 from the flat image
    These are the columns of the phase_stepping_curve
    input, while the row is the pixel number."""
    n_phase_steps = phase_stepping_curve.shape[0]
    transformed = np.delete(phase_stepping_curve, -1, axis=0)
    transformed = np.fft.rfft(transformed, axis=0)
    a0 = np.abs(transformed[0, :]) 
    a1 = np.abs(transformed[n_periods, :]) 
    phi1 = np.unwrap(np.angle(transformed[n_periods, :]))
    if flat:
        a0_flat, phi_flat, a1_flat = flat
        a0 /= a0_flat
        phi1 -= phi_flat
        a1 /= a1_flat / a0
    return a0, phi1, a1

if __name__ == '__main__':
    args = commandline_parser.parse_args()
    root_file_name = args.file[0]
    flat_file_name = args.flat[0]
    n_lines = args.lines[0]
    pixel_file = args.pixel_file[0]
    pixel = int(open(pixel_file).read()) 
    object_name = "postprocessing/stack_pixel_{0}_{0}".format(
            pixel)
    extension = args.format[0]
    roi = args.roi
    root_file = ROOT.TFile(root_file_name, "update")
    if not root_file.IsOpen():
        raise IOError("Could not open {0}.".format(
            root_file_name))
    histogram = root_file.Get(object_name)
    if not histogram:
        raise IOError("Object {0} not found.".format(
            object_name))
    flat_root_file = ROOT.TFile(flat_file_name, "update")
    if not root_file.IsOpen():
        raise IOError("Could not open {0} for flat.".format(
            root_file_name))
    flat_histogram = flat_root_file.Get(object_name)
    if not histogram:
        raise IOError("Object {0} not found for flat.".format(
            object_name))
    image_array = th2_to_numpy(histogram)[:,roi[0]:roi[1]]
    flat_image = th2_to_numpy(flat_histogram)[:,roi[0]:roi[1]]
    flat_parameters = get_signals(flat_image)
    images = np.split(image_array, n_lines, axis=0)
    absorption_image = np.zeros((n_lines, image_array.shape[1]))
    differential_phase_image = np.zeros_like(absorption_image)
    dark_field_image = np.zeros_like(absorption_image)
    for i, phase_stepping_curve in enumerate(images):
        absorption, phase, dark_field = get_signals(
                phase_stepping_curve,
                flat_parameters)
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
    img2.set_clim(-1, math.pi)
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
    plt.savefig(root_file_name.replace(".root",
        "." + extension))
    plt.show()
