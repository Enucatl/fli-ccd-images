"""Commandline parser for stack-related operations."""

from readimages.raw_images.commandline_parser import commandline_parser

commandline_parser.__doc__ = "Stack all the pictures"

commandline_parser.add_argument('--pixel', metavar='PIXEL',
        nargs='?', default=509, type=int,
        help='default pixel number')
commandline_parser.add_argument('--format', metavar='FORMAT',
        nargs='?', default="tif", help='output format')
commandline_parser.add_argument('--roi', metavar=('min', 'max'),
        nargs=2, default=[300, 800],
        type=int, help='region of interest')
