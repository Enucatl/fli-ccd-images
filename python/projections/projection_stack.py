#!/usr/bin/env python

from __future__ import division, print_function

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from raw_images.base_rootfile_analyser import BaseRootfileAnalyser
from projections.commandline_parser import commandline_parser

class ProjectionStackMaker(BaseRootfileAnalyser):
    """Draw a stack of a projection along a pixel of all the images in the ROOT file"""
    def __init__(self, pixel, *args, **kwargs):
        super(ProjectionStackMaker, self).__init__(*args, **kwargs)
        self.pixel = pixel
        """check pixel list: it must contain 1 or 2 values"""
        if len(pixel) == 1:
            pixel.append(pixel[0])
        elif len(pixel) == 2 and not pixel[1]:
            pixel[1] = pixel[0]
        elif len(pixel) > 2 or len(pixel) == 0:
            print("one or two pixel numbers (begin and end) must be specified!")
            raise IOError

    def output_name(self):
        return "stack_pixel_{0[0]}_{0[1]}".format(self.pixel)

    def if_not_exists(self):
        super(ProjectionStackMaker, self).if_not_exists()
        self.tree.GetEntry(0)
        example_image = self.tree.image
        title = "{0} along pixel {1[0]}-{1[1]}; x pixel; image number".format(
                self.root_file.GetName(),
                self.pixel)
        self.n_bins_x = example_image.GetNbinsX()
        self.output_object = ROOT.TH2D(self.output_name(), title,
                self.n_bins_x,
                example_image.GetXaxis().GetXmin(),
                example_image.GetXaxis().GetXmax(),
                self.n_images,
                0,
                self.n_images)
        first_pixel = int(example_image.GetYaxis().GetBinLowEdge(1))
        self.projection_pixel = [int(x) - first_pixel for x in self.pixel]

    def analyse_histogram(self, i, hist):
        super(ProjectionStackMaker,
                self).analyse_histogram(i, hist)
        projection = hist.ProjectionX("_px", self.projection_pixel[0],
                self.projection_pixel[1])
        for j in range(self.n_bins_x):
            self.output_object.SetBinContent(j + 1, i + 1,
                    projection.GetBinContent(j + 1))

    def close(self):
        try:
            if not self.batch:
                self.canvas = ROOT.TCanvas("canvas", "canvas")
                self.output_object.Draw("col")
                print()
                raw_input("press ENTER to quit")
        except KeyboardInterrupt:
            pass
        finally:
            super(ProjectionStackMaker, self).close()

if __name__ == '__main__':
    from readimages_utils.rootstyle import tdrstyle_grayscale
    from readimages_utils.hadd import hadd
    tdrstyle_grayscale()
    args = commandline_parser.parse_args()
    root_file_name = hadd(args.file)
    overwrite = args.overwrite
    use_corrected = args.corrected
    pixel_file = args.pixel_file[0]
    pixel = int(open(pixel_file).read()) 
    batch = args.batch
    open_option = "update"

    with ProjectionStackMaker([pixel], root_file_name,
            open_option,
            use_corrected,
            overwrite,
            batch) as analyser:
        if not analyser.exists_in_file:
            for i, entry in enumerate(analyser.tree):
                branch_name = analyser.branch_name
                histogram = getattr(entry, branch_name)
                analyser.analyse_histogram(i, histogram)
        else:
            pass
