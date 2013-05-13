#!/usr/bin/env python
from __future__ import division, print_function

import os
import argparse

import h5py

import math
import numpy as np
from scipy import ndimage
from skimage import io
from skimage import filter
from skimage import img_as_uint

from projections.commandline_parser import commandline_parser
from readimages_utils.hadd import hadd
from raw_images.base_analyser import post_processing_dirname

def split_indices(array):
    """Find the grating position as the indices where the array change from
    0 to 1."""
    indices = np.flatnonzero(array)
    split_points = [indices[0]]
    for i in range(len(indices) - 1):
        if indices[i] + 1 != indices[i + 1]:
            split_points.append(indices[i] + 1)
            split_points.append(indices[i + 1])
    return split_points

def grating_height(segments):
    """From a list of arrays:
    zeros
    upper edge of the grating
    zeros
    lower edge of the grating
    zeros
    holder
    
    Return the upper edge, lower_edge (averages) of the grating and
    the sum of the standard deviations of the two.
    """
    upper_edge = segments[1]
    lower_edge = segments[3]
    empty_distance = segments[2].shape[0]

    upper_positions = np.array(range(upper_edge.shape[0]))
    upper_average = np.average(upper_positions,
            weights=upper_edge)
    upper_variance = np.dot(upper_edge, (upper_positions - upper_average)**2)/upper_edge.sum()  # Fast and numerically precise
    lower_positions = np.array(range(lower_edge.shape[0]))
    lower_average = np.average(lower_positions,
            weights=lower_edge)
    lower_variance = np.dot(lower_edge, (lower_positions - lower_average)**2)/lower_edge.sum()  # Fast and numerically precise

    upper_position = segments[0].shape[0] + upper_average
    lower_position = segments[0].shape[0] + upper_edge.shape[0] + empty_distance + lower_average
    std_dev = math.sqrt(lower_variance + upper_variance)
    return upper_position, lower_position, std_dev

if __name__ == '__main__':
    commandline_parser.add_argument('--split', metavar='N_SUB_IMAGES',
            nargs=1, type=int, default=[1],
            help='split the original image into N subimages.')
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
    x = np.zeros(n_images)
    y = np.zeros(n_images)
    yerr = np.zeros(n_images)
    lower_edges = []
    upper_edges = []
    processed_images = []
    image_height = 0
    for i, image in enumerate(images):
        image = image[:, roi[0]:roi[1]]
        image_height = image.shape[0]
        edges = filter.sobel(image)
        threshold = filter.threshold_otsu(edges)
        label_objects, nb_labels = ndimage.label(edges > threshold)
        sizes = np.bincount(label_objects.ravel())
        mask_sizes = sizes > (roi[1] - roi[0])
        mask_sizes[0] = 0
        cleaned = mask_sizes[label_objects]
        filled = ndimage.binary_fill_holes(cleaned)
        summed = np.sum(filled, axis=1)
        output_name = object_name.replace("/", "_")
        output_name = "{0}_{1}.{2}".format(
                output_name,
                i, extension)
        segments = np.split(summed, split_indices(summed))
        if len(segments) < 4:
            continue
        upper_edge, lower_edge, std_dev = grating_height(segments)
        height = lower_edge - upper_edge
        x[i] = i
        y[i] = height
        yerr[i] = std_dev / math.sqrt(roi[1] - roi[0])
        lower_edges.append(lower_edge)
        upper_edges.append(upper_edge)
        processed_images.append(filled)
    print(processed_images)
    processed_images = np.reshape(processed_images, (-1, (roi[1] - roi[0])))
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    plt.tight_layout()
    ax1.imshow(image_array, cmap=plt.cm.Greys_r)
    ax2.imshow(processed_images, cmap=plt.cm.Greys_r)
    for i, (lower_edge, upper_edge) in enumerate(
            zip(lower_edges, upper_edges)):
        first_pixel = i * image_height
        ax2.axhline(y=(first_pixel + lower_edge), color='r')
        ax2.axhline(y=(first_pixel + upper_edge), color='r')
    plt.figure()
    plt.errorbar(x, y, fmt='o')
    plt.ion()
    plt.show()
    print()
    raw_input("Press ENTER to quit.")
