#!/usr/bin/env python
from __future__ import division, print_function
import array
import os
from itertools import islice

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from raw_images.base_rootfile_analyser import BaseRootfileAnalyser

class ImageConverter(BaseRootfileAnalyser):
    """Convert all raw images in the tree to an image format with ROOT::TAsImage."""
    def __init__(self, extension, root_file_name, *args, **kwargs):
        super(ImageConverter,
                self).__init__(root_file_name, *args, **kwargs)
        self.extension = extension.lower()
        self.parent_dir, _ = os.path.splitext(root_file_name)
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
        n_colors = 900
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

        hist_array = array.array("d")
        for i in range(self.height):
            start = 1 + (i + 1) * (self.width + 2)
            sliced = islice(histogram.fArray, start,
                    start + self.width)
            hist_array.extend(sliced)
        self.image.SetImage(hist_array,
                self.width,
                self.height,
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

if __name__ == '__main__':
    from raw_images.commandline_parser import commandline_parser
    from utils.rootstyle import tdrstyle_grayscale
    from utils.hadd import hadd

    commandline_parser.description = ImageConverter.__doc__
    commandline_parser.add_argument('--format', metavar='FORMAT',
            nargs=1, default=["gif"], help='format of the images to be stored')
    args = commandline_parser.parse_args()
    root_file_name = hadd(args.file)
    extension = args.format[0]
    overwrite = args.overwrite
    use_corrected = args.corrected
    open_option = "update"
    tdrstyle_grayscale()
    with ImageConverter(extension, root_file_name) as analyser:
        if not analyser.exists_in_file:
            for i, entry in enumerate(analyser.tree):
                branch_name = analyser.branch_name
                histogram = getattr(entry, branch_name)
                analyser.analyse_histogram(i, histogram)
        else:
            pass
