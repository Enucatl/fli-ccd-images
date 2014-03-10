"""

"""

from __future__ import division, print_function

import numpy as np

from readimages.utils.progress_bar import progress_bar
from readimages.raw_images.base_analyser import BaseHDF5Analyser

def get_projection_stack(files, pixel,
        roi, overwrite):
    """Factory of projection stacks."""
    psm = ProjectionStackMaker(pixel,
            files,
            "a",
            use_corrected=False,
            overwrite=overwrite,
            batch=True)
    psm.open()
    if not psm.exists_in_file:
        #Make projection stack if it doesn't exist.
        for i, image in enumerate(psm.images.values()):
            psm.analyse_histogram(i, image)
    projection_stack = psm.output_object[:, roi[0]:roi[1]]
    psm.close()
    return projection_stack

class ProjectionStackMaker(BaseHDF5Analyser):
    """Draw a stack of a projection along a pixel of all the images in the
    file.

    """
    def __init__(self, pixel, *args, **kwargs):
        self.pixel = pixel
        super(ProjectionStackMaker, self).__init__(*args, **kwargs)
        example_image = next(iter(self.images.values()))
        self.dtype = example_image.dtype
        first_pixel = example_image.attrs["min_y"]
        last_pixel = example_image.attrs["max_y"]
        self.max_x = example_image.attrs["max_x"]
        self.min_x = example_image.attrs["min_x"]
        self.projection_pixel = self.pixel - first_pixel
        self.corrected_pixels = 0
        if self.pixel > last_pixel:
            raise IOError("max pixel is {0}, cannot get pixel {1}".format(
                last_pixel, self.pixel))

    def output_name(self):
        return "stack_pixel_{0}".format(self.pixel)

    def if_not_exists(self):
        super(ProjectionStackMaker, self).if_not_exists()
        self.title = "{0} along pixel {1}; x pixel; image number".format(
                self.input_file.filename,
                self.pixel)
        width = self.max_x - self.min_x
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
            self.corrected_pixels += line[
                    line > mean + 3 * std_dev].shape[0]
            line[line > mean + 3 * std_dev] = mean
        self.output_object[i, :] = line

    def dont_start(self):
        print("projection_stack: result already saved in file.")
        print(progress_bar(1))

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
                        "pixels corrected (/{0} total pixels, {1:.3%})".format(
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
                input("Press ENTER to quit.")
        except KeyboardInterrupt:
            pass
        finally:
            super(ProjectionStackMaker, self).close()
