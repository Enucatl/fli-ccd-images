"Reconstruct the dpc_scan macro"

from __future__ import division, print_function

from readimages.dpc.dpc_scan_reconstructor import ScanReconstructor
from readimages.dpc.commandline_parser import commandline_parser

if __name__ == '__main__':
    commandline_parser.add_argument('--flats_every', 
            nargs='?', type=int, default=999999,
            help='flats taken every N_FLATS steps')
    commandline_parser.add_argument('--n_flats', metavar='N_FLATS',
            nargs='?', type=int, default=5,
            help='how many flats to average')
    args = commandline_parser.parse_args()
    dpcr = ScanReconstructor(args.file,
            args.pixel,
            args.roi,
            args.steps,
            args.periods,
            args.flats_every,
            args.n_flats,
            args.format,
            args.overwrite)
    dpcr.reconstruct()
    if not args.batch:
        dpcr.draw()
    dpcr.save()
