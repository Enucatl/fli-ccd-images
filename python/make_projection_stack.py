#!/usr/bin/env python

from __future__ import division, print_function
import sys

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from base_rootfile_analyser import BaseRootfileAnalyser, commandline_parser
from rootstyle import tdrstyle_grayscale

tdrstyle_grayscale()

class ProjectionStackMaker(BaseRootfileAnalyser):
    """Draw a stack of a projection along a pixel of all the images in the ROOT file"""
    def __init__(self, pixel, *args, **kwargs):
        super(ProjectionStackMaker, self).__init__(*args, **kwargs)
        self.pixel = pixel
        """check pixel list: it must contain 1 or 2 values"""
        if len(pixel) == 1:
            pixel.append(pixel[0])
        elif len(pixel) > 2 or len(pixel) == 0:
            print("one or two pixel numbers (begin and end) must be specified!")
            raise IOError

    def __enter__(self):
        super(ProjectionStackMaker, self).__enter__()
        stack_name = "stack_pixel_{0[0]}_{0[1]}".format(pixel)
        #self.stack = self.directory.Get(stack_name)
        self.stack = 0
        if not self.stack:
            self.stack_exists_in_file = False
            title = "{0} along pixel {1[0]}-{1[1]}; x pixel; image number".format(
                    self.root_file.GetName(),
                    self.pixel)
            self.n_bins_x = self.example_histogram.GetNbinsX()
            self.stack = ROOT.TH2D(stack_name, title,
                    self.n_bins_x,
                    self.example_histogram.GetXaxis().GetXmin(),
                    self.example_histogram.GetXaxis().GetXmax(),
                    self.n_images,
                    0,
                    self.n_images)
            first_pixel = int(self.example_histogram.GetYaxis().GetBinLowEdge(1))
            self.pixel = [int(x) - first_pixel for x in self.pixel]
        else:
            self.stack_exists_in_file = True
        return self

    def __iter__(self):
        if self.stack_exists_in_file:
            "don't start iteration if stack already exists"
            print("stack exists in file, drawing it")
            return []
        else:
            return super(ProjectionStackMaker, self).__iter__()

    def analyse_histogram(self, i, hist):
        super(ProjectionStackMaker,
                self).analyse_histogram(i, hist)
        projection = hist.ProjectionX("_px", self.pixel[0], self.pixel[1])
        for j in range(self.n_bins_x):
            self.stack.SetBinContent(j + 1, i + 1,
                    projection.GetBinContent(j + 1))

    def write(self):
        #result = self.stack.Write()
        v = ROOT.TVectorD(1)
        v[0] = 10
        print()
        self.directory.cd()
        print(v.Write("v", ROOT.TObject.kOverwrite))
        self.directory.ls()

    def __exit__(self, exc_type, exc_value, traceback):
        print()
        print("calling exit")
        print(exc_type, exc_value, traceback)
        #print(not not self.directory)
        #self.directory.cd()
        #self.stack.Write()
        #self.root_file.Close()
        #self.canvas = ROOT.TCanvas("canvas", "canvas")
        #self.stack.Draw("col")
        try:
            pass
            #raw_input()
        except KeyboardInterrupt:
            super(ProjectionStackMaker, self).__exit__(
                    exc_type, exc_value, traceback)
            print("Got CTRL+C, closing...")
        finally:
            super(ProjectionStackMaker, self).__exit__(
                exc_type, exc_value, traceback)
        
commandline_parser.description = ProjectionStackMaker.__doc__
commandline_parser.add_argument('pixel', metavar='PIXEL',
        nargs='+', help='pixel number(s)')

if __name__ == '__main__':
    args = commandline_parser.parse_args()
    root_file_name = args.file[0]
    pixel = commandline_parser.parse_args().pixel

    with ProjectionStackMaker(pixel, root_file_name) as analyser:
        for i, hist in analyser:
            analyser.analyse_histogram(i, hist)
        analyser.write()
    print()
    print()
    print("file")
    root_file_read = ROOT.TFile(root_file_name)
    root_file_read.ls()
    print()
    print("dir")
    directory = root_file_read.Get("postprocessing")
    print(not not directory)
    directory.ls()
