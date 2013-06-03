#!/usr/bin/env python
from __future__ import division, print_function

import os
import argparse

import matplotlib.pyplot as plt
import h5py

import readimages_utils.rcparams
from projections.projection_stack import get_projection_stack
from projections.commandline_parser import commandline_parser
from readimages_utils.hadd import hadd

"""Export a dataset to an image."""

commandline_parser.description = __doc__
commandline_parser.add_argument('--dataset', metavar='DATASET',
        nargs='+', default=['postprocessing/stack_pixel_510'],
        help='dataset(s) in the HDF5 file to be exported')
commandline_parser.add_argument('--show', action='store_true',
        help='show each image.')

if __name__ == '__main__':
    args = commandline_parser.parse_args()
    extension = args.format[0]
    dataset_names = args.dataset
    file_name = hadd(args.file)
    input_file = h5py.File(file_name, "r")
    n = len(dataset_names)
    print('saving {0} images:'.format(n))
    for i, name in enumerate(dataset_names):
        image_array = input_file[name]
        output_name = "{0}.{1}".format(
                name, extension)
        without_slashes = output_name.replace("/", "_")
        full_output_path = file_name.replace(".hdf5", "_" + without_slashes)
        print(full_output_path)
        plt.imsave(full_output_path, image_array)
        if args.show:
            plt.figure()
            plt.imshow(image_array)
            plt.ion()
            plt.show()
            raw_input("Press ENTER to continue.")
    print()
    print("Done!")
    print()
