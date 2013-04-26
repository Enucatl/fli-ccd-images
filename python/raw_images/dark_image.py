#!/usr/bin/env python
# encoding: utf-8

from __future__ import division, print_function

import numpy as np

from raw_images.image_combination import ImageCombination

def calculate_dark(list_of_images):
    """Calculate the master dark image as the MEDIAN of the indicated
    dark images.

    """
    arrays = []
    result = list_of_images[0].Clone()
    n_bins = result.fN
    for image in list_of_images:
        arrays.append(np.array(
            [image.fArray[i] for i in range(n_bins)],
            dtype=np.int16))
    median_array = np.median(arrays, axis=0)
    for i in range(n_bins):
        result.fArray[i] = median_array[i]
    result.SetEntries(n_bins)
    return result

class DarkImageCalculator(ImageCombination):
    """Descriptor.
    Calculate dark image from a list of images."""

    def __init__(self):
        ImageCombination.__init__(self)

    def __set__(self, obj, list_of_images):
        self.image = calculate_dark(list_of_images)
