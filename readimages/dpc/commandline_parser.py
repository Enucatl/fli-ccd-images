"""Commandline parser for dpc reconstruction."""

from readimages.projections.commandline_parser import commandline_parser

commandline_parser.add_argument('--steps', metavar='STEPS',
        nargs='?', type=int, default=8,
        required=True,
        help='number of phase steps')
commandline_parser.add_argument('--periods', metavar='PERIODS',
        nargs='?', type=int, default=1,
        help='number of phase stepping periods')
