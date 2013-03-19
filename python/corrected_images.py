#!/usr/bin/env python
# encoding: utf-8

from __future__ import division, print_function
from base_rootfile_analyser import BaseRootfileAnalyser, commandline_parser
import ROOT

def image_name(config, section):
    first = config.getint(section, "first_image")
    last = config.getint(section, "last_image")
    return "{0}_image_{1}_{2}".format(section, first, last)

class CorrectedTree(BaseRootfileAnalyser):
    """Add a tree with corrected images to the file."""

    def __init__(self, config, *args, **kwargs):
        """the ConfigParser should contain the information needed to find
        dark and a flat images. These should be already saved in the file!

        """
        BaseRootfileAnalyser.__init__(self, *args, **kwargs)
        self.dark_image = self.directory.Get(dark_image_name(config, "dark"))
        self.flat_image = self.directory.Get(flat_image_name(config, "flat"))

        if not self.dark_image or not self.flat_image:
            raise IOError("No dark or flat in file!")

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
    from ConfigParser import ConfigParser
    with CorrectedTree(config, root_file_name) as analyser:
        if not analyser.exists_in_file:
            for i, entry in enumerate(analyser.tree):
                analyser.analyse_histogram(i, entry.image)
        else:
            pass
