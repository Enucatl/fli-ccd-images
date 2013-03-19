#!/usr/bin/env python
# encoding: utf-8

from __future__ import division, print_function
from image_combination import ImageCombination
import numpy

class DarkImageCalculator(ImageCombination):
    """Calculate dark image from consecutive images stored in a tree."""

    def __init__(self, *args, **kwargs):
        ImageCombination.__init__(self, *args, **kwargs)

    def output_name(self):
        return "dark_image_{0}_{1}".format(
                self.first_index,
                self.last_index)

    def calculate_output(self):
        """Calculate the master dark image as the MEDIAN of the indicated
        dark images.

        """
        arrays = []
        for i in range(self.first_index, self.last_index + 1):
            super(ImageCombination, self).analyse_histogram(i, 0)
            self.tree.GetEntry(i)
            cpp_array = self.tree.image.fArray
            arrays.append(numpy.array(
                [cpp_array[i] for i in range(self.n_bins)],
                dtype=numpy.int16))
        median_array = numpy.median(arrays, axis=0)
        for i in range(self.n_bins):
            self.output_object.fArray[i] = median_array[i]
        self.output_object.SetEntries(self.n_bins)

if __name__ == '__main__':
    root_file_name = "test.root"
    first_index = 0
    last_index = 1
    with DarkImageCalculator(
            root_file_name,
            first_index,
            last_index) as dic:
        pass
