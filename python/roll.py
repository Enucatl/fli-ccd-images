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
        nargs=1, default=["postprocessing/stack_pixel_515_515"],
        help='name of the histogram')
commandline_parser.add_argument('--split', metavar='N_SUB_IMAGES',
        nargs=1, type=int, default=[1],
        help='split the original image into N subimages (default 1).')
commandline_parser.add_argument('--format', metavar='FORMAT',
        nargs=1, default=["tif"], help='output format (default 16bit tif)')

if __name__ == '__main__':
    args = commandline_parser.parse_args()
    root_file_name = args.file[0]
    object_name = args.object[0]
    extension = args.format[0]
    n_subimages = args.split[0]
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
    images = np.split(image_array, n_subimages, 0)
    io.use_plugin("freeimage")
    n_images = len(images)
    columns = 3
    edge_array = []
    #images = [images[4]]
    for i, image in enumerate(images):
        image = image[:, 300:900]
        #thresholded = image < 3100
        edges = filter.sobel(image)
        edge_array.append(edges)
    #plt.savefig(output_name, bbox_inches=0)
    edge_array = np.reshape(edge_array, (-1, 600))
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    plt.subplots_adjust(left=0.0, right=1.0, bottom=0.0, top=0.95)
    ax1.imshow(image_array, cmap=plt.cm.Greys_r)
    ax1.set_title("original")
    ax2.imshow(edge_array, cmap=plt.cm.Greys_r)
    ax2.set_title("sobel filter")
    plt.show()
