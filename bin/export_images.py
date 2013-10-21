#!/usr/bin/env python

"""Convert HDF5 images to any image format supported by matplotlib."""

from __future__ import division, print_function
import os
import shutil

import matplotlib.pyplot as plt
from readimages.raw_images.base_analyser import BaseHDF5Analyser
from readimages.utils.hadd import hadd
from readimages.print_version import print_version

class ImageConverter(BaseHDF5Analyser):
    """Convert all raw images in to an image format."""
    def __init__(self, extension, file_name, *args, **kwargs):
        self.extension = extension.lower()
        self.parent_dir, _ = os.path.splitext(hadd(file_name))
        self.image_dir = os.path.join(self.parent_dir, self.extension)
        super(ImageConverter,
                self).__init__(file_name, *args, **kwargs)

    def output_name(self):
        return self.image_dir
    
    def output_exists(self, name):
        return os.path.exists(name)

    def if_not_exists(self):
        """Make output folder"""
        if os.path.exists(self.image_dir):
            shutil.rmtree(self.image_dir)
        os.makedirs(self.image_dir)
        super(ImageConverter, self).if_not_exists()

    def analyse_histogram(self, i, name, hist):
        super(ImageConverter, self).analyse_histogram(i, hist)
        plt.imshow(hist,
                origin='lower',
                )
        output_file_name = "{0}.{1}".format(name, extension)
        plt.imsave(os.path.join(self.output_name(), output_file_name),
                hist)


    def close(self):
        print()
        print("created image files in", self.output_name())
        print()

if __name__ == '__main__':
    from readimages.raw_images.commandline_parser import commandline_parser
    print_version(commandline_parser.prog)

    commandline_parser.description = ImageConverter.__doc__
    commandline_parser.add_argument('--format', metavar='FORMAT',
            nargs=1, default=["tif"], help='output format')
    args = commandline_parser.parse_args()
    extension = args.format[0]
    overwrite = args.overwrite
    use_corrected = args.corrected
    open_option = "r"
    with ImageConverter(extension,
            args.file,
            open_option,
            use_corrected,
            overwrite) as analyser:
        if not analyser.exists_in_file:
            for i, (name, histogram) in enumerate(analyser.images.iteritems()):
                analyser.analyse_histogram(i, name, histogram)
        else:
            pass
