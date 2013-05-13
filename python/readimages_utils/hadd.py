#!/usr/bin/env python
# encoding: utf-8

from __future__ import division, print_function

import os

import h5py
import raw_images

def hadd(files):
    """Merge several files into one.
    
    Return the name of the output file.
    """

    if len(files) == 1:
        """Nothing to do with only one input file."""
        return files[0]
    else:
        dir_name = os.path.dirname(files[0])
        first_name = os.path.splitext(os.path.basename(files[0]))[0]
        last_name = os.path.splitext(os.path.basename(files[-1]))[0]
        output_name = "{0}_{1}.hdf5".format(
                first_name, last_name)
        """Don't overwrite"""
        if not os.path.exists(output_name_with_dir):
            output_name_with_dir = os.path.join(dir_name, output_name)
            output_file = h5py.File(output_name_with_dir, "w-")
            output_group = output_file.create_group(raw_images.base_analyser.raw_images_group)
            for input_file_name in files:
                input_file = h5py.File(input_file_name, "r")
                for name, data in input_file[raw_images_group].iteritems():
                    group.create_dataset(name, data=data)
                input_file.close()
            output_file.close()
        return output_name_with_dir

if __name__ == '__main__':
    from raw_images.commandline_parser import commandline_parser
    args = commandline_parser.parse_args()
    output_file = hadd(args.file)
    print(output_file)
