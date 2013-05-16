#!/usr/bin/env python

from __future__ import division, print_function

import numpy as np

from raw_images.base_analyser import BaseHDF5Analyser
from projections.commandline_parser import commandline_parser

def get_projection_stack(files, args):
    """Factory of projection stacks."""
    psm = ProjectionStackMaker(args.pixel[0],
            files,
            "a",
            args.corrected,
            args.overwrite,
            batch=True)
    psm.open()
    if not psm.exists_in_file:
        """Make projection stack if it doesn't exist."""
        for i, image in enumerate(psm.images.itervalues()):
            psm.analyse_histogram(i, image)
    projection_stack = psm.output_object[:, args.roi[0]:args.roi[1]]
    psm.close()
    return projection_stack

class ProjectionStackMaker(BaseHDF5Analyser):
    """Draw a stack of a projection along a pixel of all the images in the
    file.
    
    """
    def __init__(self, pixel, *args, **kwargs):
        self.pixel = pixel + 1
        super(ProjectionStackMaker, self).__init__(*args, **kwargs)
        example_image = self.images.itervalues().next()
        self.dtype = example_image.dtype
        first_pixel = example_image.attrs["max_y"]
        self.max_x = example_image.attrs["max_x"]
        self.min_x = example_image.attrs["min_x"]
        self.projection_pixel = first_pixel - self.pixel
        self.corrected_pixels = 0

    def output_name(self):
        return "stack_pixel_{0}".format(self.pixel)

    def if_not_exists(self):
        super(ProjectionStackMaker, self).if_not_exists()
        self.title = "{0} along pixel {1}; x pixel; image number".format(
                self.input_file.filename,
                self.pixel)
        width = self.max_x - self.min_x
        """with respect to the ROOT version, this histogram has swapped axes
        and the pixel number for the projection is the ROOT number + 1"""
        self.output_object = np.zeros(
                (self.n_images, width),
                dtype=self.dtype)

    def analyse_histogram(self, i, hist):
        super(ProjectionStackMaker,
                self).analyse_histogram(i, hist)
        line = hist[self.projection_pixel, :] 
        mean = np.mean(line)
        std_dev = np.std(line)
        if (line > mean + 3 * std_dev).any():
            line[line > mean + 3 * std_dev] = mean
            self.corrected_pixels += 1
        self.output_object[i, :] = line

    def close(self):
        try:
            if not self.batch:
                import matplotlib.pyplot as plt
                print()
                if self.corrected_pixels:
                    shape = self.output_object.shape
                    total_pixels = shape[0] * shape[1]
                    print("direct conversions in the ccd:",
                        self.corrected_pixels,
                        "pixels corrected (on {0} total pixels, {1:.3%})".format(
                            total_pixels,
                            self.corrected_pixels / total_pixels))
                plt.figure()
                plt.imshow(self.output_object,
                        origin='lower',
                        extent=[self.min_x, self.max_x,
                            0, self.n_images],
                        aspect='auto')
                print()
                plt.ion()
                plt.show()
                raw_input("Press ENTER to quit.")
        except KeyboardInterrupt:
            pass
        finally:
            super(ProjectionStackMaker, self).close()

if __name__ == '__main__':
    args = commandline_parser.parse_args()
    file_name = args.file
    overwrite = args.overwrite
    use_corrected = args.corrected
    pixel = args.pixel[0]
    batch = args.batch
    open_option = "a"

    with ProjectionStackMaker(pixel, file_name,
            open_option,
            use_corrected,
            overwrite,
            batch) as analyser:
        if not analyser.exists_in_file:
            for i, image in enumerate(analyser.images.itervalues()):
                analyser.analyse_histogram(i, image)
        else:
            pass
