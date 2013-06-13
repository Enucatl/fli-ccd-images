#!/usr/bin/env python

"""Measure the roll of the grating, that is the rotation along the x axis.

"""

from __future__ import division, print_function

import numpy as np
from skimage import io
from skimage import filter
import matplotlib.pyplot as plt

from projections.commandline_parser import commandline_parser
from projections.projection_stack import get_projection_stack

if __name__ == '__main__':
    commandline_parser.add_argument('--split', metavar='N_SUB_IMAGES',
            nargs=1, type=int, default=[1],
            help='split the original image into N subimages (default 1).')
    args = commandline_parser.parse_args()
    roi = args.roi
    image_array = get_projection_stack(args.file, args)
    images = np.split(image_array, args.split[0], 0)
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
    ax1.imshow(image_array)
    ax1.set_title("original")
    ax2.imshow(edge_array)
    ax2.set_title("sobel filter")
    plt.ion()
    plt.show()
    raw_input("Press ENTER to quit.")
