#!/usr/bin/env python

"""Reconstruct the three grating interferometry signals.

"""

from __future__ import division, print_function

from readimages.dpc.image_reconstructor import ImageReconstructor
from readimages.dpc.commandline_parser import commandline_parser


commandline_parser.description = ImageReconstructor.__doc__

if __name__ == '__main__':
    import pkg_resources
    version = pkg_resources.require("readimages")[0].version
    print("\n", commandline_parser.prog, version, end="\n\n")

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
