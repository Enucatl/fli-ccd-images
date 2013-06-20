#!/usr/bin/env python

"""Perform a computed tomography reconstruction from a sinogram
(--dataset) with the gridrec program.

"""

from __future__ import division, print_function

import tempfile
import os
import h5py
import numpy as np
import subprocess
import matplotlib.pyplot as plt

import readimages_utils.rcparams #pylint: disable=W0611
from readimages_utils.hadd import hadd

from tomography.commandline_parser import commandline_parser

commandline_parser.description = __doc__

if __name__ == '__main__':
    args = commandline_parser.parse_args()
    filter_name = args.filter
    rotation_centre = args.centre
    dataset_names = args.dataset
    file_name = hadd(args.file)
    input_file = h5py.File(file_name, "a")
    overwrite = args.overwrite
    n = len(dataset_names)
    for i, name in enumerate(dataset_names):
        output_name = "{0}_gridrec_reconstruction_{1}".format(
                name, rotation_centre)
        if output_name in input_file and not overwrite:
            reconstructed_image = input_file[output_name]
        else:
            if output_name in input_file and overwrite:
                del input_file[output_name]
            image_array = input_file[name][...].astype(np.float32)
            width = image_array.shape[0]
            height = image_array.shape[1]
            header = np.array(
                    [height, width,
                    width * height], dtype=np.uint16)
            _, temporary_dmp_name = tempfile.mkstemp(suffix=".DMP")
            temporary_dmp = open(temporary_dmp_name, "wb")
            header.tofile(temporary_dmp)
            image_array.tofile(temporary_dmp)
            temporary_dmp.close()
            gridrec_command = "gridrec -f {0}\
                    -c {1}\
                    -g 2 -t 0 -Z 1 -O / -D /\
                    {2}".format(
                            filter_name,
                            rotation_centre,
                            temporary_dmp_name)
                    #the dirs -D / -O / have to be specified,
                    #otherwise gridrec assumes
                    #that the file is in the current directory
            print("calling gridrec")
            print(gridrec_command)
            subprocess.check_call(gridrec_command, shell=True)
            os.remove(temporary_dmp_name)
            reconstructed_name = temporary_dmp_name.replace(".DMP", ".rec.DMP")
            reconstructed_file = open(reconstructed_name, "rb")
            reconstructed_header = np.fromfile(
                    reconstructed_file,
                    dtype=np.uint16, count=3)
            reconstructed_image = np.fromfile(
                    reconstructed_file,
                    dtype=np.float32)
            reconstructed_image = np.reshape(reconstructed_image,
                    (reconstructed_header[0],
                    reconstructed_header[1]))
            reconstructed_file.close()
            os.remove(reconstructed_name)
            input_file.create_dataset(output_name, data=reconstructed_image)
            if args.show:
                plt.figure()
                plt.imshow(reconstructed_image)
                plt.ion()
                plt.show()
                raw_input("Press ENTER to continue.")
            input_file.close()
