#!/usr/bin/env python
from __future__ import division, print_function
import numpy
import os
from glob import glob
from skimage.io import imread, imread_collection, imsave
from matplotlib import pyplot, cm
from skimage.exposure import rescale_intensity
from skimage import img_as_float
from progress_bar import progress_bar

def post_process(globbing_pattern, flat_image):
    print("analyzing", globbing_pattern)
    file_names = glob(globbing_pattern)
    n = len(file_names)
    for i, file_name in enumerate(file_names):
        print(progress_bar(i/n), end="")
        directory = os.path.dirname(file_name)
        basename = os.path.basename(file_name)
        parent_directory = os.path.dirname(directory)
        new_dir = os.path.join(parent_directory, "postprocessed")
        new_name = os.path.join(new_dir, basename)
        try:
            os.mkdir(new_dir)
        except OSError:
            pass
        imsave(new_name, rescale_intensity(
            img_as_float(imread(file_name, as_grey=True)) / flat_image
            ))
    print()
    print()


flat_images = [
"/home/abis_m/afsproject/raw_data/2012/nickel89/tif2/nickel_flat0002.tif",
"/home/abis_m/afsproject/raw_data/2012/nickel89/tif2/nickel_flat0005.tif",
"/home/abis_m/afsproject/raw_data/2012/nickel89/tif2/nickel_flat0003.tif",
"/home/abis_m/afsproject/raw_data/2012/nickel89/tif2/nickel_flat0006.tif",
"/home/abis_m/afsproject/raw_data/2012/nickel89/tif2/nickel_flat0004.tif",
        ]

nickel_images_pattern = "/home/abis_m/afsproject/raw_data/2012/nickel89/tif2/nickel00*tif"
gold1_images_pattern = "/home/abis_m/afsproject/raw_data/2012/gold15/tif/gold0001.tif"
gold2_images_pattern = "/home/abis_m/afsproject/raw_data/2012/gold3/tif/gold15_part*tif"

flat_images = [img_as_float(imread(name, as_grey=True)) for name in flat_images]
flat_image = flat_images[0]
pyplot.imshow(flat_images[0], cmap=cm.gray)
for image in flat_images[1:]:
    flat_image = numpy.add(flat_image, image)

flat_image /= len(flat_images)

pyplot.imshow(flat_image, cmap=cm.gray)

post_process(nickel_images_pattern, flat_image)
post_process(gold1_images_pattern, flat_image)
post_process(gold2_images_pattern, flat_image)

#pyplot.show()
