#!/usr/bin/env python
from __future__ import division, print_function

import os

import h5py
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import iradon

import readimages_utils.rcparams
from raw_images.base_analyser import post_processing_dirname
from readimages_utils.hadd import hadd


from tomography.commandline_parser import commandline_parser

"""Perform a computed tomography reconstruction from a sinogram
(--dataset) with the filtered back projection (skimage.transform.iradon)

http://scikit-image.org/docs/dev/api/skimage.transform.html#iradon

"""

commandline_parser.description = __doc__

if __name__ == '__main__':
    dataset_names = args.dataset
    file_name = hadd(args.file)
    input_file = h5py.File(file_name, "a")
    overwrite = args.overwrite
    n = len(dataset_names)
    projections = args.projections[0]
    angles = np.linspace(args.angles[0], args.angles[1], projections)
    for i, name in enumerate(dataset_names):
        sinogram = input_file[name]
        output_name = name + "_ct_reconstruction"
        output_dataset = input_file.require_dataset(output_name)
        if output_name in input_file and not overwrite:
            print("tomography:",
            name, "already saved in file.")
            continue
        else:
            output_dataset = iradon(sinogram,
                    angles,
                    filer='hamming',
                    interpolation='linear')
            print()
            print("Done!")
            print()
        input_file.close()
        if args.show:
            plt.figure()
            plt.imshow(output_dataset)
            plt.ion()
            plt.show()
            raw_input("Press ENTER to continue.")
