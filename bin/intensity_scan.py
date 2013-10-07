#!/usr/bin/env python

from __future__ import division, print_function

import matplotlib.pyplot as plt
import numpy as np

from readimages.raw_images.base_analyser import BaseHDF5Analyser

class IntensityScan(BaseHDF5Analyser):
    """Plot the intensity as a function of the
    image number in a folder (e.g. a scan).
    
    """
    def __init__(self, roi, *args, **kwargs):
        self.roi = roi
        super(IntensityScan, self).__init__(*args, **kwargs)
        x_min, x_max, y_min, y_max = roi
        self.check_roi(x_min, x_max, y_min, y_max)
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def check_roi(self, x_min, x_max, y_min, y_max):
        """check that the passed arguments are sensible and inside the image
        range"""
        example_image = self.images.itervalues().next()
        if x_min > x_max:
            print("x_min must be less than x_max")
            raise IOError
        if y_min > y_max:
            print("y_min must be less than y_max")
            raise IOError
        if x_min < example_image.attrs["min_x"]:
            print("x_min out of the range of the image")
            raise IOError
        if x_max > example_image.attrs["max_x"]:
            print("x_max out of the range of the image")
            raise IOError
        if y_min < example_image.attrs["min_y"]:
            print("y_min out of the range of the image")
            raise IOError
        if y_max > example_image.attrs["max_y"]:
            print("y_max out of the range of the image")
            raise IOError

    def output_name(self):
        return "intensity_scan_{0}x{1}_{2}x{3}".format(*self.roi)

    def if_not_exists(self):
        super(IntensityScan, self).if_not_exists()
        self.y = np.zeros(len(self.images))
        self.x = np.arange(1, len(self.images) + 1)

    def analyse_histogram(self, i, hist):
        """add integral and image number to graph"""
        super(IntensityScan, self).analyse_histogram(i, hist)
        self.y[i] = np.sum(hist[
            self.y_min - hist.attrs["min_y"]:
            self.y_max - hist.attrs["min_y"],
            self.x_min:
            self.x_max
            ])

    def close(self):
        if not self.batch:
            plt.figure()
            plt.errorbar(self.x, self.y,
                    yerr=np.sqrt(self.y), fmt='o')
            plt.xlabel("file number")
            plt.ylabel("intensity (integral)")
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            plt.ion()
            plt.show()
            try:
                print()
                raw_input("press ENTER to quit")
            except KeyboardInterrupt:
                pass
            finally:
                super(IntensityScan, self).close()

if __name__ == '__main__':
    from readimages.raw_images.commandline_parser import commandline_parser
    commandline_parser.description = IntensityScan.__doc__
    commandline_parser.add_argument('--roi',
        metavar=('min_x', 'max_x', 'min_y', 'max_y'),
        nargs=4, type=int, help='min_x max_x min_y max_y')
    args = commandline_parser.parse_args()
    overwrite = True
    use_corrected = args.corrected
    open_option = "a"
    with IntensityScan(args.roi, args.file,
            open_option, use_corrected,
            overwrite, args.batch) as analyser:
        if not analyser.exists_in_file:
            for i, image in enumerate(analyser.images.itervalues()):
                analyser.analyse_histogram(i, image)
        else:
            pass
