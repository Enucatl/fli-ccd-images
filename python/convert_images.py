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
            if image_file_name == ".":
                image_file_name, _ = os.path.splitext(self.root_file.GetName())
            image_file_name = os.path.join(self.image_dir, image_file_name)
            image_file_name += "." + self.extension
        else:
            image_file_name = os.path.join(self.image_dir, "")
        return image_file_name
    
    def output_exists(self, name):
        return os.path.exists(name)

    def if_not_exists(self):
        """Make output folder"""
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)
        super(ImageConverter, self).if_not_exists()
        self.tree.GetEntry(0)
        self.width = self.tree.rows
        self.height = self.tree.columns
        n_colors = 256
        self.palette = tdrstyle_grayscale(n_colors)
        self.palette = ROOT.TImagePalette(n_colors,
                self.palette)
        self.image = ROOT.TASImage(self.width, self.height)

    def analyse_histogram(self, i, hist):
        super(ImageConverter, self).analyse_histogram(i, hist)
        write_as = self.output_name()
        if self.extension == "gif":
            if i < (self.n_images - 1):
                write_as += "+30" #+30ms per image
            else:
                write_as += "++1" #1 loop
        else:
            write_as = self.output_name() + hist.GetName() + "." + self.extension
        """convert th2d to image as in tutorial
        http://root.cern.ch/root/html534/tutorials/image/hist2image.C.html"""

        hist_array = array.array("d",
                (hist.fArray[i] for i in xrange(hist.fN)))
        self.image.SetImage(hist_array,
                self.width + 2,
                self.height + 2,
                self.palette)
        self.image.WriteImage(write_as)

    def close(self):
        print()
        if extension == "gif":
            print("created gif file", self.output_name())
        else:
            print("created image files in", self.output_name())
        print()
        self.root_file.Close()

commandline_parser.description = ImageConverter.__doc__
commandline_parser.add_argument('--format', metavar='FORMAT',
        nargs=1, default=["gif"], help='format of the images to be stored, default GIF')

if __name__ == '__main__':
    args = commandline_parser.parse_args()
    root_file_name = args.file[0]
    extension = args.format[0]
    with ImageConverter(extension, root_file_name) as analyser:
        if not analyser.exists_in_file:
            for i, entry in enumerate(analyser.tree):
                analyser.analyse_histogram(i, entry.image)
        else:
            pass
