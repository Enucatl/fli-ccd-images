"""Commandline parser for dpc reconstruction."""

from projections.commandline_parser import commandline_parser

commandline_parser.add_argument('--flat', metavar='FLAT_FILE.hdf5',
        nargs='+', 
        help='hdf5 file(s) with the histogram for the flat field')
commandline_parser.add_argument('--flats_every', metavar='N_FLATS',
        nargs='?', type=int, default=999999,
        help='flats taken every N_FLATS steps')
commandline_parser.add_argument('--steps', metavar='STEPS',
        nargs=1, type=int, default=8,
        required=True,
        help='number of phase steps')
commandline_parser.add_argument('--periods', metavar='PERIODS',
        type=int, default=1,
        help='number of phase stepping periods')
