#!/usr/bin/env python
from __future__ import division, print_function

import os
import argparse

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from rootstyle import tdrstyle_grayscale
from iterate_over_histograms import HistogramIterator
from progress_bar import progress_bar

tdrstyle_grayscale()
commandline_parser = argparse.ArgumentParser(description='''Base class for doing
        something with all the TH2 in a ROOT file.''')
commandline_parser.add_argument('file', metavar='FILE.root',
        nargs=1, help='ROOT file with the TH2 histograms')

"""save results of calculations in this TDirectory inside the ROOT file"""
post_processing_dirname = "postprocessing"

class BaseRootfileAnalyser(object):
    """abstract base class to perform the same operation over all the TH2
    in the same ROOT file, with appropriate setup (enter) and cleanup
    (exit) functions, and a loop over all the histograms.
    
    These functions are meant to be redefined in daughter classes."""
    def __init__(self, root_file_name,
            open_option="update"):
        super(BaseRootfileAnalyser, self).__init__()
        if not os.path.exists(root_file_name):
            print("File not found", root_file_name)
            raise IOError
        self.root_file = ROOT.TFile(root_file_name, open_option)
        "create directory for output if not in read mode"
        if open_option != "read":
            self.directory = self.root_file.Get(post_processing_dirname)
            if not self.directory:
                self.directory = self.root_file.mkdir(post_processing_dirname)
        print("initialized base")
        
    def __enter__(self):
        self.iterator = HistogramIterator(self.root_file)
        try:
            self.example_histogram = self.iterator[0]
        except IndexError:
            print("No images found in file",
                    self.root_file.GetName())
            raise IOError
        self.n_images = len(self.iterator)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print()
        print("Done!")
        print()
        v = ROOT.TVectorD(1)
        v[0] = 10
        print()
        self.directory.cd()
        print(v.Write("v", ROOT.TObject.kOverwrite))
        self.directory.ls()
        print("closing root file")
        self.root_file.Close()

    def __iter__(self):
        print()
        print("Analysing", self.n_images, "images...")
        """iterate over 'self' as
        for i, hist in self:
            self.analyse_histogram(i, hist)
            because the index i is always useful,
            at least for the progress bar"""
        return enumerate(self.iterator)

    def analyse_histogram(self, i, hist):
        """base version just prints the progress bar advancement for
        the index i"""
        print(progress_bar((i + 1) / self.n_images), end='')

if __name__ == '__main__':
    args = commandline_parser.parse_args()
    root_file_name = args.file[0]
    with BaseRootfileAnalyser(root_file_name) as base_analyser:
        for i, hist in base_analyser:
            base_analyser.analyse_histogram(i, hist)
