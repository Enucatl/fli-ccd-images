#!/usr/bin/env python
# encoding: utf-8

from __future__ import division, print_function
from base_rootfile_analyser import BaseRootfileAnalyser, commandline_parser
from dark_image import DarkImageCalculator
from flat_image import FlatImageCalculator
import numpy
import operator
import ROOT

def get_dark_flat_images(config):
    """Return a list whose indices are the indices of the images in the
    tree,
    the values are "is_dark" if the image is a dark image
    "is_flat" if the image is a flat image,
    "is_normal" otherwise.

    :config: a ConfigParser object used to take the scan
    :returns: the list

    """
    section = "scan"
    n_dark_images = config.getint(section, "n_dark_images")
    take_flat_every = config.getint(section, "take_flat_every")
    raw_scan_parameters = [line.strip().split()
                for line in config.get(section,
                    "scan_motors").splitlines()]
    images_per_motor = [
            int(intervals) + 1
            for motor_name, begin, end, intervals in raw_scan_parameters]
    flat_counter = 0
    n_flat_images = config.getint(section, "n_flat_images")
    if take_flat_every:
        flat_counter = reduce(operator.mul, images_per_motor[:-1])
        flat_counter *= take_flat_every
        steps_in_outermost_loop = images_per_motor[-1]
        n_flats = (steps_in_outermost_loop) // take_flat_every
        total_flat_images = n_flats * n_flat_images
    n_images = reduce(operator.mul, images_per_motor)

    result = ["is_dark" for _ in range(n_dark_images)]
    for i in range(n_images):
        if flat_counter and not i % flat_counter:
            result += ["is_flat"] * n_flat_images
        result.append("is_normal")
    #for i, item in enumerate(result):
        #print(i, item)
    return result

class CorrectedTree(BaseRootfileAnalyser):
    """Add a tree with corrected images to the file."""

    dark_image = DarkImageCalculator()
    flat_image = FlatImageCalculator()

    def __init__(self, config, root_file_name, open_option="update"):
        """the ConfigParser should contain the information needed to 
        tell which images are dark or flat images.

        """
        BaseRootfileAnalyser.__init__(self, root_file_name, open_option)
        self.list_of_indices = get_dark_flat_images(config)
        self.dark_images = []
        self.flat_images = []

    def output_name(self):
        return "corrected_image_tree"

    def if_not_exists(self):
        super(CorrectedTree, self).if_not_exists()
        self.output_object = ROOT.TTree(
                self.output_name(),
                self.output_name())

        self.tree.GetEntry(0)
        self.corrected_image = self.tree.image

        self.is_dark_or_flat = numpy.array([True], dtype=numpy.bool_)
        self.output_object.Branch("corrected_image", self.corrected_image)
        self.output_object.Branch("is_dark_or_flat", self.is_dark_or_flat,
                "is_dark_or_flat/O")

    def analyse_histogram(self, i, hist):
        """Subtract dark and divide by flat."""
        super(CorrectedTree, self).analyse_histogram(i, hist)
        self.tree.GetEntry(i)
        non_corrected_image = self.tree.image
        if self.list_of_indices[i] == "is_dark":
            self.is_dark_or_flat = True
            self.dark_images.append(non_corrected_image)
            if self.list_of_indices[i + 1] != "is_dark":
                self.dark_image = self.dark_images
                self.dark_images = []
        elif self.list_of_indices[i] == "is_flat":
            self.is_dark_or_flat = True
            self.flat_images.append(non_corrected_image)
            if self.list_of_indices[i + 1] != "is_dark":
                self.flat_image = self.flat_images
                self.flat_images = []
        else:
            self.is_dark_or_flat = False
            self.corrected_image.Add(non_corrected_image, self.dark_image,
                    1, -1)
            self.corrected_image.Divide(self.flat_image)
        self.output_object.Fill()

    def close(self):
        self.output_object.AddFriend(self.tree.GetName())
        super(CorrectedTree, self).close()

commandline_parser.description = CorrectedTree.__doc__
commandline_parser.add_argument('--config',
        nargs='?', default='../spec_macros/python/config/default_config.ini', help='config.ini file with dark/flat info')

if __name__ == '__main__':
    args = commandline_parser.parse_args()
    root_file_name = args.file[0]
    config_file_name = args.config
    from ConfigParser import ConfigParser
    config = ConfigParser()
    config.read(config_file_name)

    with CorrectedTree(config, root_file_name) as analyser:
        if not analyser.exists_in_file:
            for i, entry in enumerate(analyser.tree):
                analyser.analyse_histogram(i, entry.image)
        else:
            pass
