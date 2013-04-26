"""Command line parser for all the analysers of raw images (saved in a
TTree)."""

import argparse

commandline_parser = argparse.ArgumentParser(description='''Base class for doing
        something with all the TH2 in a ROOT file.''',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
commandline_parser.add_argument('file', metavar='FILE.root',
        nargs='+', help='ROOT file(s) with the tree')
commandline_parser.add_argument('--batch', '-b', 
        action='store_true',
        help='batch mode (no drawing)')
commandline_parser.add_argument('--corrected', '-c', 
        action='store_true',
        help='use dark and flat corrected images.')
commandline_parser.add_argument('--overwrite', '-o', 
        action='store_true',
        help='overwrite target if it exists')
