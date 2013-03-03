#!/usr/bin/env python
from __future__ import division, print_function
import array
import os

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from base_rootfile_analyser import BaseRootfileAnalyser, commandline_parser
from rootstyle import tdrstyle_grayscale

tdrstyle_grayscale()

class ImageConverter(BaseRootfileAnalyser):
    """convert all images to an image format, defaults to GIF"""
    def __init__(self, extension, root_file_name, *args, **kwargs):
        super(ImageConverter,
                self).__init__(root_file_name, *args, **kwargs)
        self.extension = extension.lower()
        self.parent_dir = os.path.dirname(root_file_name)
        self.image_dir = os.path.join(self.parent_dir, extension)

    def output_name(self):
        image_file_name = ""
        if self.extension == "gif":
            image_file_name = os.path.basename(
                        os.path.normpath(self.parent_dir))
            image_file_name = os.path.join(self.image_dir, image_file_name)
            image_file_name += "." + self.extension
        else:
            image_file_name = os.path.join(self.image_dir, "")
        return image_file_name
    
    def output_exists(self, name):
        print("daughter exists")
        return os.path.exists(name)

    def if_not_exists(self):
        """Make output folder"""
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)
        super(ImageConverter, self).if_not_exists()
        self.width = self.example_histogram.GetNbinsX()
        self.height = self.example_histogram.GetNbinsY()
        self.palette = ROOT.gHistImagePalette
        self.image = ROOT.TASImage(width, height)

    def analyse_histogram(self, i, hist):
        write_as = self.output_name()
        if self.extension == "gif":
            if i < (n_images - 1):
                write_as += "+3" #+30ms per image
            else:
                write_as += "++1" #1 loop
        else:
            write_as = self.output_name() + hist.GetName() + "." + self.extension
        self.image.SetImage(hist.GetBuffer(),
                self.width + 2,
                self.height + 2,
                self.palette)
        print(write_as)
        self.image.WriteImage(write_as)

    def __exit__(self, exc_type, exc_value, traceback):
        print()
        if extension == "gif":
            print("created gif file", self.output_name())
        else:
            print("created image files in", self.output_name())
        print()
        self.root_file.Close()

commandline_parser.description = ImageConverter.__doc__
commandline_parser.add_argument('--format', metavar='FORMAT',
        nargs=1, default="gif", help='format of the images to be stored, default GIF')

if __name__ == '__main__':
    args = commandline_parser.parse_args()
    root_file_name = args.file[0]
    extension = args.format
    with ImageConverter(extension, root_file_name) as analyser:
        for i, hist in analyser:
            analyser.analyse_histogram(i, hist)
