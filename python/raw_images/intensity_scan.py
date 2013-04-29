#!/usr/bin/env python
from __future__ import division, print_function
import array

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from raw_images.base_rootfile_analyser import BaseRootfileAnalyser

class IntensityScan(BaseRootfileAnalyser):
    """see intensity changes across all the images in a folder (e.g. a scan) in a region of interest. Needs the ROOT file with all the RAW images inside created by bin/make_root!"""
    def __init__(self, roi, *args, **kwargs):
        super(IntensityScan, self).__init__(*args, **kwargs)
        roi = [int(x) for x in roi]
        x_min, x_max, y_min, y_max = roi
        self.check_roi(x_min, x_max, y_min, y_max)
        self.roi = roi
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def check_roi(self, x_min, x_max, y_min, y_max):
        """check that the passed arguments are sensible and inside the image
        range"""
        self.tree.GetEntry(0)
        if x_min > x_max:
            print("x_min must be less than x_max")
            raise IOError
        if y_min > y_max:
            print("y_min must be less than y_max")
            raise IOError
        if x_min < self.tree.min_x:
            print("x_min out of the range of the image")
            raise IOError
        if x_max > self.tree.max_x:
            print("x_max out of the range of the image")
            raise IOError
        if y_min < self.tree.min_y:
            print("y_min out of the range of the image")
            raise IOError
        if y_max > self.tree.max_y:
            print("y_max out of the range of the image")
            raise IOError

    def output_name(self):
        return "intensity_scan_{0}x{1}_{2}x{3}".format(*self.roi)

    def if_not_exists(self):
        super(IntensityScan, self).if_not_exists()
        self.tree.GetEntry(0)
        example_image = self.tree.image
        self.title = "intensity in roi {0}-{1} x {2}-{3};\
        file number;\
        intensity (integral)".format(*self.roi)
        self.x = []
        self.y = []
        self.x1 = example_image.GetXaxis().FindFixBin(self.x_min)
        self.x2 = example_image.GetXaxis().FindFixBin(self.x_max)
        self.y1 = example_image.GetYaxis().FindFixBin(self.y_min)
        self.y2 = example_image.GetYaxis().FindFixBin(self.y_max)

    def analyse_histogram(self, i, hist):
        """add integral and image number to graph"""
        super(IntensityScan, self).analyse_histogram(i, hist)
        integral = hist.Integral(
                self.x1,
                self.x2,
                self.y1,
                self.y2)
        self.x.append(i + 1)
        self.y.append(integral)

    def close(self):
        if self.overwrite or not self.exists_in_file:
            x = array.array("d", self.x)
            y = array.array("d", self.y)
            self.output_object = ROOT.TGraph(self.n_images, x, y)
            self.output_object.SetTitle(self.title)
            self.output_object.SetName(self.output_name())
        self.output_object.SetMarkerStyle(20)
        self.canvas = ROOT.TCanvas("canvas", "canvas")
        self.output_object.Draw("ap")
        try:
            print()
            raw_input("press ENTER to quit")
        except KeyboardInterrupt:
            print()
            print("Got CTRL+C, closing...")
        finally:
            super(IntensityScan, self).close()

if __name__ == '__main__':
    from readimages_utils.rootstyle import tdrstyle_grayscale
    from readimages_utils.hadd import hadd
    from raw_images.commandline_parser import commandline_parser
    commandline_parser.description = IntensityScan.__doc__
    commandline_parser.add_argument('--roi',
            metavar=('min_x', 'max_x', 'min_y', 'max_y'),
            nargs=4, help='min_x max_x min_y max_y')
    args = commandline_parser.parse_args()
    root_file_name = hadd(args.file)
    roi = args.roi
    overwrite = args.overwrite
    use_corrected = args.corrected
    open_option = "update"
    tdrstyle_grayscale()
    with IntensityScan(roi, root_file_name,
            open_option, use_corrected, overwrite) as analyser:
        if not analyser.exists_in_file:
            for i, entry in enumerate(analyser.tree):
                branch_name = analyser.branch_name
                histogram = getattr(entry, branch_name)
                analyser.analyse_histogram(i, histogram)
        else:
            pass