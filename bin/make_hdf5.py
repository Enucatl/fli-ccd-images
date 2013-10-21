#!/usr/bin/env python
# encoding: utf-8

"""Convert all raw images to hdf5."""

from __future__ import division, print_function

import os
import shutil
from glob import glob

import h5py
import argparse

from readimages.utils.progress_bar import progress_bar
from readimages.print_version import print_version
from readimages.raw_images.read_raw import analyse_header
from readimages.raw_images.read_raw import read_data

commandline_parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

commandline_parser.add_argument('folder',
        metavar='FOLDER(s)',
        nargs='+',
        help='''folder(s) with the raw files. If you pass multiple
        folders you will get one hdf5 file for each folder.''')
commandline_parser.add_argument('--keep', '-k',
        action='store_true',
        help='keep the RAW files.')
commandline_parser.add_argument('--overwrite', '-o',
        action='store_true',
        help='overwrite hdf5 files if they already exist.')

def main(args):
    """Iterate over the folders:
        - check that the folder is valid
        - check if the file exists (overwrite if the
            --overwrite option was specified)
        - analyse the header to save the parameters in the attributes of the
          hdf5 dataset
        - write the data as an hdf5 dataset
        - remove the folder (unless --keep is true)

    """
    output_names = []
    for folder_name in args.folder:
        if not os.path.isdir(folder_name):
            print("make_hdf5.py: not a folder:", folder_name)
            continue
        print("make_hdf5.py: converting", folder_name)
        files = glob(os.path.join(folder_name, "*.raw"))
        output_name = os.path.normpath(folder_name) + ".hdf5"
        output_names.append(output_name)
        if not os.path.exists(output_name) or args.overwrite:
            output_file = h5py.File(output_name, 'w')
        else:
            print()
            print("""make_hdf5.py: file {0} exists.
                    Run with the --overwrite (-o) flag
                    if you want to overwrite it.""".format(
                        output_name))
            print(progress_bar(1))
            print()
            continue
        group = output_file.create_group("raw_images")
        n_files = len(files)
        for i, input_file_name in enumerate(files):
            print(progress_bar((i + 1) / n_files), end="\r")
            (_, exposure_time,
                    min_x, max_x, 
                    min_y, max_y) = analyse_header(input_file_name)
            image_name = os.path.splitext(os.path.basename(input_file_name))[0]
            image = read_data(input_file_name)
            dataset = group.create_dataset(image_name, data=image)
            dataset.attrs['exposure_time'] = exposure_time
            dataset.attrs['min_x'] = min_x
            dataset.attrs['min_y'] = min_y
            dataset.attrs['max_x'] = max_x
            dataset.attrs['max_y'] = max_y
        if not args.keep:
            print("make_hdf5.py: removing", folder_name)
            shutil.rmtree(folder_name)
        output_file.close()
        print()
        print("make_hdf5.py: written", output_name)
    print("make_hdf5.py: done!")
    return output_names

if __name__ == '__main__':
    print_version(commandline_parser.prog)
    main(commandline_parser.parse_args())
