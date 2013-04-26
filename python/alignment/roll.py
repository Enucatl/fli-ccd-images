#!/usr/bin/env python
from __future__ import division, print_function

import os
import argparse

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import math
import numpy as np
from skimage import io
from skimage import filter
import matplotlib.pyplot as plt

from projection_stack.commandline_parser import commandline_parser
from projection_stack.handle_projection_stack import get_projection_stack
from utils.th2_to_numpy import th2_to_numpy
from utils.hadd import hadd

if __name__ == '__main__':
    commandline_parser.add_argument('--split', metavar='N_SUB_IMAGES',
            nargs=1, type=int, default=[1],
            help='split the original image into N subimages (default 1).')
    args = commandline_parser.parse_args()
    root_file, histogram = get_projection_stack(args)
    image_array = th2_to_numpy(histogram)
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
