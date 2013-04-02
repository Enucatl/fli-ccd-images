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
commandline_parser.add_argument('object', metavar='OBJECT',
        nargs=1, help='name of the histogram')
commandline_parser.add_argument('--split', metavar='N_SUB_IMAGES',
        nargs=1, type=int, default=[1],
        help='split the original image into N subimages (default 1).')
commandline_parser.add_argument('--format', metavar='FORMAT',
        nargs=1, default=["tif"], help='output format (default 16bit tif)')

def split_indices(array):
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
    grid = gridspec.GridSpec(2 * (len(images) // 5 + 1), 5,
            hspace=0.01)
    x = np.zeros(n_images)
    y = np.zeros(n_images)
    yerr = np.zeros(n_images)
    for i, image in enumerate(images):
        plot1 = plt.subplot(grid[(2 * i) // 5, i % 5])
        plot2 = plt.subplot(grid[(2 * i) // 5 + 1, i % 5])
        plot1.set_title("image {0}".format(i + 1))
        image = image[:, 300:800]
        edges = filter.sobel(image)
        threshold = filter.threshold_otsu(edges)
        label_objects, nb_labels = ndimage.label(edges > threshold)
        sizes = np.bincount(label_objects.ravel())
        mask_sizes = sizes > 800
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
        yerr[i] = std_dev
        plot1.imshow(image, cmap=plt.cm.Greys_r)
        plot1.axhline(y=int(upper_edge), linewidth=1, color='r')
        plot1.axhline(y=int(lower_edge), linewidth=1, color='r')
        plot2.imshow(filled, cmap=plt.cm.Greys_r)
        plot2.axhline(y=int(upper_edge), linewidth=2, color='r')
        plot2.axhline(y=int(lower_edge), linewidth=2, color='r')
    plt.figure()
    plt.errorbar(x, y, yerr=yerr, fmt='o')
    plt.figure()
    plt.errorbar(x, yerr, fmt='ro')
    plt.savefig(output_name, bbox_inches=0)
    plt.show()
