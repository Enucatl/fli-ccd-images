#!/usr/bin/env python

"""Perform a computed tomography reconstruction from a sinogram
(--dataset) with the filtered back projection (skimage.transform.iradon)

http://scikit-image.org/docs/dev/api/skimage.transform.html#iradon

"""

from __future__ import division, print_function

import h5py
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import iradon

import readimages_utils.rcparams #pylint: disable=W0611
from readimages_utils.hadd import hadd


from tomography.commandline_parser import commandline_parser

commandline_parser.description = __doc__

if __name__ == '__main__':
    args = commandline_parser.parse_args()
    dataset_names = args.dataset
    file_name = hadd(args.file)
    input_file = h5py.File(file_name, "a")
    overwrite = args.overwrite
    n = len(dataset_names)
    projections = args.projections[0]
    angles = np.linspace(args.angles[0], args.angles[1], projections)
    roi = args.roi
    for i, name in enumerate(dataset_names):
        sinogram = np.transpose(input_file[name][:, roi[0]:roi[1]])
        output_name = name + "_ct_reconstruction"
        if output_name not in input_file or overwrite:
            if output_name in input_file:
                del input_file[output_name]
            output_dataset = iradon(sinogram,
                    angles,
                    filter='hamming',
                    interpolation='linear')
            print()
            print("Done!")
            print()
        else:
            output_dataset = input_file[output_dataset]
            print("tomography:",
            name, "already saved in file.")
            continue
        input_file.close()
        if args.show:
            plt.figure()
            plt.imshow(output_dataset)
            plt.ion()
            plt.show()
            raw_input("Press ENTER to continue.")
