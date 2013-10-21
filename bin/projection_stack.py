#!/usr/bin/env python

"""Use the ProjectionStackMaker class to display a stack of all lines in the
input file(s).

""" 

from __future__ import division, print_function

from readimages.projections.commandline_parser import commandline_parser
from readimages.projections.get_projection_stack import ProjectionStackMaker
from readimages.print_version import print_version

if __name__ == '__main__':
    print_version(commandline_parser.prog)

    commandline_parser.description = ProjectionStackMaker.__doc__
    args = commandline_parser.parse_args()
    file_name = args.file
    overwrite = args.overwrite
    use_corrected = args.corrected
    pixel = args.pixel
    batch = args.batch
    open_option = "a"

    with ProjectionStackMaker(pixel, file_name,
            open_option,
            use_corrected,
            overwrite,
            batch) as analyser:
        if not analyser.exists_in_file:
            for i, image in enumerate(analyser.images.itervalues()):
                analyser.analyse_histogram(i, image)
        else:
            pass
