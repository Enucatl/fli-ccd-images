#!/usr/bin/env python
# encoding: utf-8

"""Print the mean energy of the simulated spectrum.

"""

from __future__ import division, print_function

import argparse
import numpy as np
from itertools import islice

commandline_parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
commandline_parser.add_argument('file', metavar='FILE.spec',
        nargs=1, help='file with the spectrum calculated by SpekCalc')


if __name__ == '__main__':
    args = commandline_parser.parse_args()
    file_name = args.file[0]
    spectrum_file = open(file_name)
    header_lines = 18
    spectrum_lines = islice(spectrum_file, header_lines, None)
    lines = (line.split() for line in spectrum_lines)
    spectrum = [[float(x) for x in line] for line in lines]
    array = np.array(spectrum)
    print(np.average(array[:, 0], weights=array[:, 1]))
