#!/usr/bin/env python
# encoding: utf-8

from __future__ import division, print_function
from base_rootfile_analyser import BaseRootfileAnalyser, commandline_parser
from dark_image import DarkImageCalculator
from flat_image import FlatImageCalculator
import os
import numpy
import operator
import ROOT

class ExternalFlatDarkImporter(BaseRootfileAnalyser):
    """Add a tree with corrected images to the file."""

    dark_image = DarkImageCalculator()
    flat_image = FlatImageCalculator()

    def __init__(self, root_file_name,
            flat_file_name,
            dark_file_name="", open_option="update",
            use_corrected=False,
            overwrite=False):
        """Get flat and (optionally) dark images from other root files.

        """
        BaseRootfileAnalyser.__init__(self, root_file_name, open_option)
        if not flat_file_name or not os.path.exists(flat_file_name):
            raise IOError(
                    "{0} not found!".format(flat_file_name))

        """Get flat images."""
        self.flat_file = ROOT.TFile(flat_file_name)
        flat_images_tree = self.flat_file.Get("root_image_tree")
        if not flat_images_tree:
            raise IOError("flat images not found in", flat_file_name)
        self.dark_images = []
        self.flat_images = [event.image for event in flat_images_tree]
        self.flat_image = self.flat_images

        """Get dark images."""
        if dark_file_name and os.path.exists(dark_file_name):
            self.subtract_dark = True
            self.dark_file = ROOT.TFile(dark_file_name)
            dark_images_tree = self.dark_file.Get("root_image_tree")
            if not dark_images_tree:
                raise IOError("dark images not found in", dark_file_name)
            self.dark_images = []
            self.dark_images = [event.image for event in dark_images_tree]
            self.dark_image = self.dark_images
        else:
            self.subtract_dark = False

    def output_name(self):
        return "corrected_image_tree"

    def if_not_exists(self):
        super(ExternalFlatDarkImporter, self).if_not_exists()
        self.root_file.cd()
        self.output_object = ROOT.TTree(
                self.output_name(),
                self.output_name())

        self.tree.GetEntry(0)
        self.corrected_image = ROOT.TH2D("corr000", "corr000",
                self.tree.rows,
                self.tree.min_x,
                self.tree.max_x,
                self.tree.columns,
                self.tree.min_y,
                self.tree.max_y)

        self.output_object.Branch("corrected_image", self.corrected_image)

    def analyse_histogram(self, i, hist):
        """Subtract dark and divide by flat."""
        super(ExternalFlatDarkImporter, self).analyse_histogram(i, hist)
        self.tree.GetEntry(i)
        non_corrected_image = self.tree.image
        if self.subtract_dark:
            self.corrected_image.Add(non_corrected_image, self.dark_image,
                    1, -1)
        self.corrected_image.Divide(non_corrected_image, self.flat_image)
        #set image attributes
        self.corrected_image.SetName("{0}_corrected".format(
            non_corrected_image.GetName()))
        self.corrected_image.SetTitle(non_corrected_image.GetTitle())
        self.corrected_image.GetXaxis().SetTitle(
                non_corrected_image.GetXaxis().GetTitle())
        self.corrected_image.GetYaxis().SetTitle(
                non_corrected_image.GetYaxis().GetTitle())
        self.output_object.Fill()

    def close(self):
        self.output_object.AddFriend(self.tree.GetName())
        super(ExternalFlatDarkImporter, self).close()

commandline_parser.description = ExternalFlatDarkImporter.__doc__
commandline_parser.add_argument('--flat',
        nargs=1, help='root file with the flat images')
commandline_parser.add_argument('--dark',
        nargs='?', default='', help='root file with the dark images')

if __name__ == '__main__':
    args = commandline_parser.parse_args()
    root_file_name = args.file[0]
    flat_file_name = args.flat[0]
    dark_file_name = args.dark
    overwrite = args.overwrite
    use_corrected = args.corrected
    open_option = "update"

    with ExternalFlatDarkImporter(root_file_name, flat_file_name,
            dark_file_name,
            open_option, use_corrected, overwrite) as analyser:
        if not analyser.exists_in_file:
            for i, entry in enumerate(analyser.tree):
                analyser.analyse_histogram(i, entry.image)
        else:
            pass
