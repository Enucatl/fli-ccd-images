#!/usr/bin/env python
# encoding: utf-8

"""display a raw file. If it is a dir it watches for updates and always
shows the most recent RAW file."""

from __future__ import division, print_function

import argparse
import os

import matplotlib.pyplot as plt

from readimages.raw_images.read_raw import analyse_header
from readimages.raw_images.read_raw import read_data
from readimages.print_version import print_version

if __name__ == '__main__':
    commandline_parser = argparse.ArgumentParser(__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    commandline_parser.add_argument('f',
            nargs=1,
            help='folder or file to display'
            )
    print_version(commandline_parser.prog)
    args = commandline_parser.parse_args()
    file_name = args.f[0]
    
    if os.path.isfile(file_name):
        if os.path.splitext(file_name)[1].lower() != ".raw":
            raise IOError("{0} is not a RAW file!".format(file_name))
        image = read_data(file_name)
        plt.figure()
        plt.title(file_name)
        plt.imshow(image, aspect='auto')
        plt.ion()
        plt.show()
        raw_input("Press ENTER to continue.")
    elif os.path.isdir(file_name):
        pass
    elif not os.path.exists(file_name):
        raise OSError("{0} not found!".format(file_name))
    else:
        print(file_name, "exists but is not a file or a directory")
