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

from projections.commandline_parser import commandline_parser

if __name__ == '__main__':
    commandline_parser.add_argument('--split', metavar='N_SUB_IMAGES',
            nargs=1, type=int, default=[1],
            help='split the original image into N subimages (default 1).')
    args = commandline_parser.parse_args()
    roi = args.roi
    psm = ProjectionStackMaker(args.pixel[0],
            args.file,
            "a",
            args.corrected,
            args.overwrite,
            args.batch)
    if not psm.exists_in_file:
        """Make projection stack if it doesn't exist."""
        for i, image in enumerate(psm.images.itervalues()):
            analyser.analyse_histogram(i, image)
    images = np.split(psm.output_object, args.split[0], 0)
    io.use_plugin("freeimage")
    n_images = len(images)
    columns = 3
    edge_array = []
    for i, image in enumerate(images):
        image = image[:, roi[0]:roi[1]]
        edges = filter.sobel(image)
        edge_array.append(edges)
    edge_array = np.reshape(edge_array, (-1, roi[1] - roi[0]))
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    plt.tight_layout()
    ax1.imshow(image_array, cmap=plt.cm.Greys_r)
    ax1.set_title("original")
    ax2.imshow(edge_array, cmap=plt.cm.Greys_r)
    ax2.set_title("sobel filter")
    plt.ion()
    plt.show()
    raw_input("Press ENTER to quit.")
