#!/usr/bin/env python
from __future__ import division, print_function

import os
import argparse

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import math
from itertools import islice
import numpy as np
from scipy import ndimage
from scipy import stats
from skimage import io
from skimage import filter
from skimage import transform
from skimage import morphology
from skimage import img_as_uint
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from rootstyle import tdrstyle_grayscale
from progress_bar import progress_bar
from base_rootfile_analyser import commandline_parser
from hadd import hadd

commandline_parser.add_argument('--pixel_file', metavar='INI_FILE',
        nargs=1, default=["data/default_pixel.ini"],
        help='file containing the default pixel height')
commandline_parser.add_argument('--format', metavar='FORMAT',
        nargs=1, default=["tif"], help='output format')

if __name__ == '__main__':
    args = commandline_parser.parse_args()
    root_file_name = hadd(args.file)
    pixel_file = args.pixel_file[0]
    pixel = int(open(pixel_file).read()) 
    object_name = "postprocessing/stack_pixel_{0}_{0}".format(
            pixel)
    extension = args.format[0]
    root_file = ROOT.TFile(root_file_name, "update")
    if not root_file.IsOpen():
        raise IOError("Could not open {0}.".format(
            root_file_name))
    histogram = root_file.Get(object_name)
    if not histogram:
        raise IOError("Object {0} not found.".format(
            object_name))
    width = histogram.GetNbinsX()
    height = histogram.GetNbinsY()
    image = np.fromiter(
            (histogram.fArray[i]
                for i in range(histogram.fN)),
            dtype=np.uint16,
            count=histogram.fN)
    image_array = img_as_uint(image)
    image_array = np.reshape(image_array, (height + 2, width + 2))
    image_array = np.delete(image_array, (0, height + 1), 0)
    image_array = np.delete(image_array, (0, width + 1), 1)
    image_array = np.flipud(image_array)
    io.use_plugin("freeimage")
    output_name = root_file_name.replace(".root", "." + extension)
    io.imsave(output_name, image_array)
