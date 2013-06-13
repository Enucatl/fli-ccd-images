"""Commandline parser for tomographic reconstruction."""

from projections.commandline_parser import commandline_parser

commandline_parser.add_argument('--show', action='store_false',
        help='show the reconstructed image.')
commandline_parser.add_argument('--dataset', metavar='DATASET',
        nargs='+', default=['postprocessing/stack_pixel_510'],
        help='dataset(s) in the HDF5 file containing the sinogram')
commandline_parser.add_argument('--angles',
        metavar=('MIN_ANGLE', 'MAX_ANGLE'),
        nargs=2, default=[0, 360], type=int,
        help='dataset(s) in the HDF5 file containing the sinogram')
commandline_parser.add_argument('--projections', '-p',
        metavar='PROJECTIONS',
        nargs=1, default=[721], type=int,
        help='number of projections')
