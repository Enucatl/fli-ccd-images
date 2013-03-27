#!/usr/bin/env python
from __future__ import division, print_function

import os
import argparse

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from itertools import islice
import skimage
from skimage import filter, io
import numpy
import matplotlib.pyplot as plt

from rootstyle import tdrstyle_grayscale
from progress_bar import progress_bar

commandline_parser = argparse.ArgumentParser(description='''
        Convert object to image.''')
commandline_parser.add_argument('file', metavar='FILE.root',
        nargs=1, help='ROOT file with the histogram')
commandline_parser.add_argument('object', metavar='OBJECT',
        nargs=1, help='name of the histogram')
commandline_parser.add_argument('--format', metavar='FORMAT',
        nargs=1, default=["png"], help='output format')


if __name__ == '__main__':
    args = commandline_parser.parse_args()
    root_file_name = args.file[0]
    object_name = args.object[0]
    extension = args.format[0]
    root_file = ROOT.TFile(root_file_name)
    if not root_file.IsOpen():
        raise IOError("Could not open {0}.".format(
            root_file_name))
    histogram = root_file.Get(object_name)
    if not histogram:
        raise IOError("Object {0} not found.".format(
            object_name))
    n_colors = 999
    width = histogram.GetNbinsX()
    height = histogram.GetNbinsY()
    image = numpy.fromiter(
            (histogram.fArray[i]
                for i in range(histogram.fN)),
            dtype=numpy.uint16,
            count=histogram.fN)
    image = skimage.img_as_uint(image)
    image = numpy.reshape(image, (height + 2, width + 2))
    image = numpy.delete(image, (0, height + 1), 0)
    image = numpy.delete(image, (0, width + 1), 1)
    image = numpy.flipud(image)
    images = numpy.split(image, 13, 0)
    #edges = filter.sobel(image, sigma=4)
    image = images[3]
    edges = filter.sobel(image)
    output_name = object_name.replace("/", "_") + "." + extension
    plt.subplot(121)
    plt.imshow(image, cmap=plt.cm.Greys_r)
    plt.subplot(122)
    plt.imshow(edges, cmap=plt.cm.Greys_r)
    io.imsave(output_name, image)
    plt.show()
