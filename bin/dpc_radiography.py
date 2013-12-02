#!/usr/bin/env python

"""Reconstruct the three grating interferometry signals.

"""

from __future__ import division, print_function

from readimages.dpc.image_reconstructor import ImageReconstructor
from readimages.dpc.commandline_parser import commandline_parser
from readimages.print_version import print_version


commandline_parser.description = ImageReconstructor.__doc__

if __name__ == '__main__':
    print_version(commandline_parser.prog)

    commandline_parser.add_argument('--flat', metavar='FLAT_FILE.hdf5',
            nargs='+', 
            help='hdf5 file(s) with the flat images')
    args = commandline_parser.parse_args()
    ir = ImageReconstructor(args.file, args.flat,
            args.pixel, args.roi,
            args.steps, args.periods,
            args.format, args.overwrite)
    ir.calculate_images()
    ir.correct_drift()
    ir.save_images()
    if not args.batch:
        ir.draw()
