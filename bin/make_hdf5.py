#!/usr/bin/env python
# encoding: utf-8

"""Convert all raw images to hdf5."""

from __future__ import division, print_function

import os
import shutil
from itertools import islice
from glob import glob

import h5py
import numpy as np
import argparse

from readimages.utils.progress_bar import progress_bar

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

#number of lines in a CCD FLI header
HEADER_LINES = 16

def analyse_header(input_file_name):
    """Analyse a CCD FLI header in a RAW file saved as file_name.

    Return the bytes in the header, exposure, min_x, max_x, min_y, max_y.

    """
    input_file = open(input_file_name, 'rb')
    header = list(islice(input_file, HEADER_LINES))
    header_len = len("".join(header))
    exposure_time = float(header[4].split()[-1])
    min_y, min_x, max_y, max_x = [
            int(x) for x in header[-2].split()[2:]]
    input_file.close()
    return header_len, exposure_time, min_x, max_x, min_y, max_y

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
            (header_len, exposure_time,
                    min_x, max_x, 
                    min_y, max_y) = analyse_header(input_file_name)
            input_file = open(input_file_name, 'rb')
            input_file.read(header_len + 1)
            image_name = os.path.splitext(os.path.basename(input_file_name))[0]
            image = np.reshape(
                    np.fromfile(input_file, dtype=np.uint16),
                    (max_y - min_y, max_x - min_x),
                    order='FORTRAN')
            dataset = group.create_dataset(image_name, data=image)
            dataset.attrs['exposure_time'] = exposure_time
            dataset.attrs['min_x'] = min_x
            dataset.attrs['min_y'] = min_y
            dataset.attrs['max_x'] = max_x
            dataset.attrs['max_y'] = max_y
            input_file.close()
        if not args.keep:
            print("make_hdf5.py: removing", folder_name)
            shutil.rmtree(folder_name)
        output_file.close()
        print()
        print("make_hdf5.py: written", output_name)
    print("make_hdf5.py: done!")
    return output_names

if __name__ == '__main__':
    import pkg_resources
    version = pkg_resources.require("readimages")[0].version
    print("\n", commandline_parser.prog, version, end="\n\n")

    main(commandline_parser.parse_args())
