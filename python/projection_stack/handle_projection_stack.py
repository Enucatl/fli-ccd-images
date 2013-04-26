#!/usr/bin/env python
# encoding: utf-8

from __future__ import division, print_function

"""Generic functions for doing something with a projection stack."""

import os

import ROOT

from projection_stack.projection_stack import ProjectionStackMaker
from utils.hadd import hadd

def get_projection_stack(commandline_args):
    """Get the projection stack. Build it if necessary.
    Return the root file (otherwise it will be garbage
    collected) and the projection stack as the original TH2."""
    root_file_name = hadd(commandline_args.file)
    pixel_file = commandline_args.pixel_file[0]
    pixel = int(open(pixel_file).read()) 
    use_corrected = commandline_args.corrected
    overwrite = commandline_args.overwrite
    open_option = "update"
    projection_stack_maker = ProjectionStackMaker([pixel],
            root_file_name,
            open_option,
            use_corrected, overwrite, batch=True)
    projection_stack_maker.open()
    if not projection_stack_maker.exists_in_file:
        for i, entry in enumerate(projection_stack_maker.tree):
            branch_name = projection_stack_maker.branch_name
            histogram = getattr(entry, branch_name)
            projection_stack_maker.analyse_histogram(i, histogram)
    object_name = os.path.join(projection_stack_maker.directory.GetName(),
            projection_stack_maker.output_name())
    projection_stack_maker.close()
    root_file = ROOT.TFile(root_file_name, "update")
    if not root_file.IsOpen():
        raise IOError("Could not open {0}.".format(
            root_file_name))
    histogram = root_file.Get(object_name)
    if not histogram:
        raise IOError("Object {0} not found.".format(
            object_name))
    return root_file, histogram

if __name__ == '__main__':
    from rootstyle import tdrstyle_grayscale
    args = commandline_parser.parse_args()
    root_file, histogram = get_projection_stack(args)
    tdrstyle_grayscale()
    histogram.Draw("col")
    raw_input()
