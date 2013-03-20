#!/usr/bin/env python
# encoding: utf-8

from __future__ import division, print_function
from base_rootfile_analyser import BaseRootfileAnalyser, commandline_parser
from dark_image import DarkImageCalculator
from flat_image import FlatImageCalculator
import ROOT

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

        self.output_object.Branch("corrected_image", self.corrected_image)

    def analyse_histogram(self, i, hist):
        """Subtract dark and divide by flat."""
        super(CorrectedTree, self).analyse_histogram(i, hist)
        self.tree.GetEntry(i)
        non_corrected_image = self.tree.image
        if self.list_of_indices[i] == "is_dark":
            self.dark_images.append(non_corrected_image)
            if self.list_of_indices[i + 1] != "is_dark":
                self.dark_image = self.dark_images
                self.dark_images = []
        elif self.list_of_indices[i] == "is_flat":
            self.flat_images.append(non_corrected_image)
            if self.list_of_indices[i + 1] != "is_dark":
                self.flat_image = self.flat_images
                self.flat_images = []
        else:
            self.corrected_image.Add(non_corrected_image, self.dark_image,
                    1, -1)
            self.corrected_image.Divide(self.flat_image)
            self.output_object.Fill()

    def close(self):
        self.tree.AddFriend(self.output_object.GetName())
        super(CorrectedTree, self).close()

commandline_parser.description = CorrectedTree.__doc__
commandline_parser.add_argument('--config',
        nargs='?', default='config/config.ini', help='config.ini file with dark/flat info')

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
