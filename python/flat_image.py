#!/usr/bin/env python
# encoding: utf-8

from __future__ import division, print_function
from image_combination import ImageCombination
import numpy

def calculate_flat(list_of_images, dark_image):
    """Calculate the master flat image:
        - a master dark is subtracted from each flat image
        - a mean light level is calculated for every flat image
        - the flat images are rescaled so that they have the same mean
        - the "corrected" flat images are averaged to get a master flat

    """
    n_images = len(list_of_images)
    if dark_image:
        for image in list_of_images:
            image.Add(dark_image, -1)
    integrals = [image.Integral() for image in list_of_images]
    mean_integral = numpy.mean(integrals)
    result = list_of_images[0].Clone()
    for image, integral in zip(list_of_images, integrals):
        image.Scale(mean_integral / integral)
        result.Add(image)
    result.Scale(1 / n_images)
    return result

class FlatImageCalculator(ImageCombination):
    """Descriptor. Calculate flat image.
    It can take a master dark to be subtracted,
    from object.dark_image!"""

    def __init__(self):
        ImageCombination.__init__(self)

    def __set__(self, obj, list_of_images):
        """The object can provide a dark_image."""
        dark_image = None
        if hasattr(obj, "dark_image"):
            dark_image = obj.dark_image
        return calculate_flat(list_of_images, dark_image)
