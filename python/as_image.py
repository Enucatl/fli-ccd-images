#!/usr/bin/env python
from __future__ import division, print_function

import os
import argparse
import array

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from rootstyle import tdrstyle_grayscale
from progress_bar import progress_bar

tdrstyle_grayscale()
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
    image = ROOT.TASImage(width, height)
    palette = tdrstyle_grayscale(n_colors)
    palette = ROOT.TImagePalette(n_colors,
            palette)
    image_array = array.array("d",
            (histogram.fArray[i]
                for i in range(histogram.fN)))
    image.SetImage(image_array,
            width + 2,
            height + 2,
            palette)
    image.WriteImage(object_name.replace("/", "_") + "." + extension)
