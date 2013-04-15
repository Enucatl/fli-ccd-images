#!/usr/bin/env python
# encoding: utf-8

from __future__ import division, print_function

import os
from subprocess import check_call

def hadd(files):
    """Merge several root files into one with $ROOTSYS/bin/hadd.
    
    Return the name of the output file.
    """

    if len(files) == 1:
        """Nothing to do with only one input file."""
        return files[0]
    else:
        dir_name = os.path.dirname(files[0])
        first_name = os.path.splitext(os.path.basename(files[0]))[0]
        last_name = os.path.splitext(os.path.basename(files[-1]))[0]
        output_name = "{0}_{1}.root".format(
                first_name, last_name)
        output_name_with_dir = os.path.join(dir_name, output_name)
        merge_command = "hadd {0} {1}".format(
                output_name_with_dir,
                " ".join(files))
        print(merge_command)
        check_call(merge_command, shell=True)
        return output_name_with_dir

if __name__ == '__main__':
    from base_rootfile_analyser import commandline_parser
    args = commandline_parser.parse_args()
    output_file = hadd(args.file)
    print(output_file)
