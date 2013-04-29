#!/usr/bin/env python
from __future__ import division, print_function

import os
import argparse

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from skimage import io

from readimages_utils.th2_to_numpy import th2_to_numpy
from projections.handle_projection_stack import get_projection_stack

"""Export the projection stack to an image."""

if __name__ == '__main__':
    from projections.commandline_parser import commandline_parser
    args = commandline_parser.parse_args()
    extension = args.format[0]
    root_file, histogram = get_projection_stack(args)
    image_array = th2_to_numpy(histogram)
    io.use_plugin("freeimage")
    output_name = root_file_name.replace(".root", "." + extension)
    io.imsave(output_name, image_array)
