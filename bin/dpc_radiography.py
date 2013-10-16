#!/usr/bin/env python

"""Reconstruct the three grating interferometry signals.

"""

from __future__ import division, print_function

from readimages.dpc.image_reconstructor import ImageReconstructor
from readimages.dpc.commandline_parser import commandline_parser


commandline_parser.description = ImageReconstructor.__doc__

if __name__ == '__main__':
    args = commandline_parser.parse_args()
    ir = ImageReconstructor(args)
    ir.calculate_images()
    ir.correct_drift()
    ir.save_images()
    if not args.batch:
        ir.draw()
