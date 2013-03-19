#!/usr/bin/env python
# encoding: utf-8

from __future__ import division, print_function
from image_combination import ImageCombination
import numpy

class FlatImageCalculator(ImageCombination):
    """Calculate flat image from consecutive images stored in a tree.
    It also needs a master dark to be subtracted!"""

    def __init__(self, *args, **kwargs):
        ImageCombination.__init__(self, *args, **kwargs)
        self.master_dark = self.directory.Get(
                self.output_name().replace("flat", "dark"))
        if not self.master_dark:
            print("Couldn't find dark!")
            self.master_dark = self.output_object.Clone()

    def output_name(self):
        return "flat_image_{0}_{1}".format(
                self.first_index,
                self.last_index)

    def calculate_output(self):
        """Calculate the master flat image:
            - a master dark is subtracted from each flat image
            - a mean light level is calculated for every flat image
            - the flat images are rescaled so that they have the same mean
            - the "corrected" flat images are averaged to get a master flat

        """
        integrals = []
        for i in range(self.first_index, self.last_index + 1):
            self.tree.GetEntry(i)
            integrals.append(self.tree.image.Integral())
        mean_integral = numpy.mean(integrals)

        for i in range(self.first_index, self.last_index + 1):
            super(ImageCombination, self).analyse_histogram(i, 0)
            self.tree.GetEntry(i)
            image = self.tree.image
            image.Add(self.master_dark, -1)
            image.Scale(mean_integral / integrals[i])
            self.output_object.Add(image)

        self.output_object.Scale(1 / self.n_images)

if __name__ == '__main__':
    from dark_image import DarkImageCalculator
    root_file_name = "test.root"
    first_index = 0
    last_index = 1
    dark_image_calculator = DarkImageCalculator(root_file_name,
            first_index, last_index)
    dark_image_calculator.open()
    dark_image_calculator.calculate_output()
    dark_image_calculator.close()
    with FlatImageCalculator(
                root_file_name,
                first_index,
                last_index) as flat_image_calculator:
            flat_image_calculator.output_object.Draw("col")
            #raw_input()
