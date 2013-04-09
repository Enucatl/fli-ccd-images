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

commandline_parser = argparse.ArgumentParser(description='''
        Convert object to image.''')
commandline_parser.add_argument('file', metavar='FILE.root',
        nargs=1, help='ROOT file with the histogram')
commandline_parser.add_argument('--object', metavar='OBJECT',
        nargs=1, default=["postprocessing/stack_pixel_508_508"],
        help='name of the histogram')
commandline_parser.add_argument('--format', metavar='FORMAT',
        nargs=1, default=["tif"], help='output format (default 16bit tif)')

if __name__ == '__main__':
    args = commandline_parser.parse_args()
    root_file_name = args.file[0]
    object_name = args.object[0]
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
    for i in range(width):
        projection = histogram.ProjectionY(
                "projectiony_{0}".format(i + 1),
                i + 1, i + 1, "e")
        transform = projection.FFT(0, "mag r2c ex")
        print(transform.GetBinContent(1), transform.GetBinContent(2))
