#!/usr/bin/env python
from __future__ import division, print_function

import warnings
import os
import argparse

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from rootstyle import tdrstyle_grayscale
from progress_bar import progress_bar
from hadd import hadd

tdrstyle_grayscale()
commandline_parser = argparse.ArgumentParser(description='''Base class for doing
        something with all the TH2 in a ROOT file.''',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
commandline_parser.add_argument('file', metavar='FILE.root',
        nargs='+', help='ROOT file(s) with the tree')
commandline_parser.add_argument('--batch', '-b', 
        action='store_true',
        help='batch mode (no drawing)')
commandline_parser.add_argument('--corrected', '-c', 
        action='store_true',
        help='use dark and flat corrected images.')
commandline_parser.add_argument('--overwrite', '-o', 
        action='store_true',
        help='overwrite target if it exists')

"""save results of calculations in this TDirectory inside the ROOT file"""
post_processing_dirname = "postprocessing"

class BaseRootfileAnalyser(object):
    """abstract base class to perform the same operation over all the TH2
    in the same ROOT file, with appropriate setup (open) and cleanup
    (close) functions, and a loop over all the histograms.
    
    These functions are meant to be redefined in daughter classes."""
    def __init__(self, root_file_name, open_option="update",
    use_corrected=False,
    overwrite=False,
    batch=False):
        super(BaseRootfileAnalyser, self).__init__()
        if not os.path.exists(root_file_name):
            print("File not found", root_file_name)
            raise IOError
        self.overwrite = overwrite
        self.batch = batch
        self.root_file = ROOT.TFile(root_file_name, open_option)
        self.tree = self.root_file.Get(os.path.join(
            post_processing_dirname, "corrected_image_tree"))
        if use_corrected:
            self.branch_name = "corrected_image"
            if not self.tree or not self.tree.GetEntriesFast():
                warnings.warn("""
                Could not find corrected images!
                Using the raw ones.""")
                self.tree = self.root_file.Get("root_image_tree")
                self.branch_name = "image"
        else: 
            self.tree = self.root_file.Get("root_image_tree")
            self.branch_name = "image"
            if not self.tree or not self.tree.GetEntriesFast():
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
        if self.overwrite or not self.output_exists(name):
            self.if_not_exists()
        else:
            self.if_exists()

    def __enter__(self):
        self.open()
        return self

    def close(self):
        """write output object if it did not exist and close file"""
        if self.overwrite or not self.exists_in_file:
            self.directory.cd()
            self.output_object.Write(self.output_object.GetName(),
                    ROOT.TObject.kOverwrite)
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
    root_file_name = hadd(args.file)
    overwrite = args.overwrite
    use_corrected = args.corrected
    open_option = "update"
    with BaseRootfileAnalyser(root_file_name,
            open_option,
            use_corrected,
            overwrite) as base_analyser:
        for i, event in enumerate(base_analyser.tree):
            base_analyser.analyse_histogram(i, event.image)

    root_file_open = ROOT.TFile(root_file_name)
    root_file_open.ls()
    directory = root_file_open.Get(post_processing_dirname)
    directory.ls()
