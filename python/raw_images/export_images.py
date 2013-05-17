#!/usr/bin/env python
from __future__ import division, print_function
import array
import os
from itertools import islice

import matplotlib.pyplot as plt
from raw_images.base_analyser import BaseHDF5Analyser

class ImageConverter(BaseHDF5Analyser):
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

    def analyse_histogram(self, i, name, hist):
        super(ImageConverter, self).analyse_histogram(i, hist)
        plt.imshow(hist,
                origin='lower',
                )
        plt.imsave(self.output_name() + name + self.format)


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
    from readimages_utils.rootstyle import tdrstyle_grayscale
    from readimages_utils.hadd import hadd

    commandline_parser.description = ImageConverter.__doc__
    args = commandline_parser.parse_args()
    extension = args.format[0]
    overwrite = args.overwrite
    use_corrected = args.corrected
    open_option = "update"
    tdrstyle_grayscale()
    with ImageConverter(extension, root_file_name) as analyser:
        if not analyser.exists_in_file:
            for i, (name, histogram) in
                enumerate(analyser.images.iteritems()):
                analyser.analyse_histogram(i, name, histogram)
        else:
            pass
