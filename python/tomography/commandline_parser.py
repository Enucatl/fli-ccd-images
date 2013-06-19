"""Commandline parser for tomographic reconstruction."""

from projections.commandline_parser import commandline_parser

commandline_parser.add_argument('--show', action='store_false',
        help='show the reconstructed image.')
commandline_parser.add_argument('--dataset', metavar='DATASET',
        nargs='+', default=['postprocessing/stack_pixel_510'],
        help='dataset(s) in the HDF5 file containing the sinogram')
commandline_parser.add_argument('--centre', '-r',
        metavar='CENTRE',
        help='Rotation centre as a fraction of the sinogram width.',
        nargs='?', default=0.5, type=float)
commandline_parser.add_argument('--filter', '-f',
        metavar='FILTER',
        nargs='?', default='parzen', type=str,
        help='Filter used in the reconstruction. See gridrec -h for details.')
