#!/usr/bin/env python
from __future__ import division, print_function

import os
import argparse

import matplotlib.pyplot as plt

import readimages_utils.rcparams
from projections.projection_stack import get_projection_stack
from projections.commandline_parser import commandline_parser
from readimages_utils.hadd import hadd

"""Export the projection stack to an image."""

if __name__ == '__main__':
    args = commandline_parser.parse_args()
    extension = args.format[0]
    image_array = get_projection_stack(args.file, args)
    plt.figure()
    plt.imshow(image_array)
    output_name = hadd(args.file).replace(".hdf5", "." + extension)
    plt.imsave(output_name)
    plt.ion()
    plt.show()
    raw_input("Press ENTER to quit.")
