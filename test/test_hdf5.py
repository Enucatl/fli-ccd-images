#!/usr/bin/env python
# encoding: utf-8

from __future__ import division, print_function

import sys
import os
from itertools import islice
from glob import glob
from readimages_utils.progress_bar import progress_bar

import h5py
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    folder_name = sys.argv[1]
    files = glob(os.path.join(folder_name, "*.raw"))
    output_name = os.path.normpath(folder_name) + ".hdf5"
    output_file = h5py.File(output_name, 'w')
    group = output_file.create_group("raw_images")
    header_lines = 16
    n_files = len(files)
    print(n_files)
    for i, input_file_name in enumerate(files):
        print(progress_bar((i + 1) / n_files), end="\r")
        input_file = open(input_file_name, 'rb')
        image_name = os.path.splitext(os.path.basename(input_file_name))[0]
        header = list(islice(input_file, header_lines))
        header_len = len("".join(header))
        exposure_time = float(header[4].split()[-1])
        min_y, min_x, max_y, max_x = [int(x) for x in header[-2].split()[2:]]
        input_file.close()
        input_file = open(input_file_name, 'rb')
        input_file.read(header_len + 1)
        image = np.reshape(np.fromfile(input_file, dtype=np.uint16),
                (max_y - min_y, max_x - min_x),
                order='FORTRAN')
        dataset = group.create_dataset(image_name, data=image)
        dataset.attrs['exposure_time'] = exposure_time
        dataset.attrs['min_x'] = min_x
        dataset.attrs['min_y'] = min_y
        dataset.attrs['max_x'] = max_x
        dataset.attrs['max_y'] = max_y
        show = False
        if show:
            print("".join(header))
            print(image.shape)
            print(image)
            print("exposure", exposure_time)
            plt.figure()
            plt.imshow(image, origin='lower',
                    extent=[min_x, max_x, min_y, max_y])
            plt.locator_params(axis='y', nbins=3)
            plt.show()
    output_file.close()
    print()
    print("Done!")
