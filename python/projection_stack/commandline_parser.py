from raw_images.commandline_parser import commandline_parser

commandline_parser.add_argument('--pixel_file', metavar='INI_FILE',
        nargs=1, default=["data/default_pixel.ini"],
        help='file containing the default pixel height')
commandline_parser.add_argument('--format', metavar='FORMAT',
        nargs=1, default=["tif"], help='output format')
commandline_parser.add_argument('--roi', metavar='FORMAT',
        nargs=2, default=[300, 800],
        type=int, help='region of interest')
