#!/usr/bin/env python

"""Export a dataset to an image."""

from __future__ import division, print_function

import matplotlib.pyplot as plt
import h5py

import readimages.utils.rcparams #pylint: disable=W0611
from readimages.projections.commandline_parser import commandline_parser
from readimages.utils.hadd import hadd
from readimages.print_version import print_version

commandline_parser.description = __doc__
commandline_parser.add_argument('--dataset', metavar='DATASET',
        nargs='+', default=['postprocessing/stack_pixel_509'],
        help='dataset(s) in the HDF5 file to be exported')
commandline_parser.add_argument('--show', action='store_true',
        help='show each image.')

if __name__ == '__main__':
    print_version(commandline_parser.prog)

    args = commandline_parser.parse_args()
    extension = args.format
    dataset_names = args.dataset
    file_name = hadd(args.file)
    input_file = h5py.File(file_name, "r")
    n = len(dataset_names)
    print('saving {0} images:'.format(n))
    for i, name in enumerate(dataset_names):
        try:
            image_array = input_file[name]
        except KeyError:
            print(name, "not found!\n\n")
            raise
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
