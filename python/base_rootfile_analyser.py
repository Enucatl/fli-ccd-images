#!/usr/bin/env python
from __future__ import division, print_function

import warnings
import os
import argparse

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from rootstyle import tdrstyle_grayscale
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
    def __init__(self, root_file_name, open_option="update"):
        super(BaseRootfileAnalyser, self).__init__()
        if not os.path.exists(root_file_name):
            print("File not found", root_file_name)
            raise IOError
        self.root_file = ROOT.TFile(root_file_name, open_option)
        self.tree = self.root_file.Get(os.path.join(
            post_processing_dirname, "corrected_image_tree"))
        if not self.tree and not self.tree.GetEntriesFast():
            warnings.warn("""Could not find corrected images!
            Using the raw ones.""")
            self.tree = self.root_file.Get("root_image_tree")
        if not self.tree and not self.tree.GetEntriesFast():
            print("Tree not found or empty", "root_image_tree")
            raise IOError

        "create directory for output if not in read mode"
        if open_option != "read":
            self.directory = self.root_file.Get(post_processing_dirname)
            if not self.directory:
                self.directory = self.root_file.mkdir(post_processing_dirname)
        self.n_images = self.tree.GetEntriesFast()
        
    def output_name(self):
        """get name of output ROOT object produced"""
        return "NotImplemented"

    def if_not_exists(self):
        """do some initialization if output object was not found in the input file"""
        self.exists_in_file = False

    def if_exists(self):
        """do some initialization if output object was  found in the input file"""
        self.dont_start()
        self.exists_in_file = True

    def dont_start(self):
        print("result already saved in file.")
        print(progress_bar(1), end="")
        print()

    def output_exists(self, name):
        self.output_object = self.directory.Get(name)
        "not not trick to convert ROOT object to bool"
        return not not self.output_object

    def open(self):
        name = self.output_name()
        if not self.output_exists(name):
            self.if_not_exists()
        else:
            self.if_exists()

    def __enter__(self):
        self.open()
        return self

    def close(self):
        """write output object if it did not exist and close file"""
        if not self.exists_in_file:
            self.directory.cd()
            self.output_object.Write()
        print()
        print("Done!")
        print()
        self.root_file.Close()

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            import traceback
            print(exc_type, exc_value, traceback.print_tb(tb))
        self.close()

    def analyse_histogram(self, i, hist):
        """base version just prints the progress bar advancement for
        the index i"""
        print(progress_bar((i + 1) / self.n_images), end='')

if __name__ == '__main__':
    args = commandline_parser.parse_args()
    root_file_name = args.file[0]
    with BaseRootfileAnalyser(root_file_name) as base_analyser:
        for i, event in enumerate(base_analyser.tree):
            base_analyser.analyse_histogram(i, event.image)

    root_file_open = ROOT.TFile(root_file_name)
    root_file_open.ls()
    directory = root_file_open.Get(post_processing_dirname)
    directory.ls()
