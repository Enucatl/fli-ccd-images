#!/usr/bin/env python
from __future__ import division, print_function
from rootstyle import tdrstyle_grayscale
import ROOT

class RawImageReader(object):
    """read raw image as saved by the Proline CCD camera in the PSI east
    lab.
    Store it as a ROOT 2d histogram.
    Uses c++ function defined in read_raw_image.C"""
    def __init__(self, file_name):
        super(RawImageReader, self).__init__()
        self.file_name = file_name
        input_file = open(file_name, "rb")
        text = input_file.read()
        input_file.close()
        text = text.split("\n")
        header_bytes = self.process_header(text)
        self.init_image(header_bytes)
        
    def process_header(self, text):
        self.rows = 0
        self.columns = 0
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0
        total_header_lines = 0
        for i, line in enumerate(text):
            total_header_lines += 1
            if "rows" in line:
                self.rows = int(line.split()[2])
            elif "columns" in line:
                self.columns = int(line.split()[2])
            elif "ROI" in line:
                self.min_x, self.min_y, self.max_x, self.max_y = (int(x)
                        for x in line.split()[2:])
            elif "EOH" in line:
                break
        header_bytes = len("".join(text[:total_header_lines])) + 1
        return header_bytes

    def init_image(self, header_bytes):
        ROOT.gROOT.ProcessLine(".L read_raw_image.C+")
        tdrstyle_grayscale()
        self.image = ROOT.TH2I(self.file_name, self.file_name,
                self.rows,
                self.min_x,
                self.max_x,
                self.columns,
                self.min_y,
                self.max_y)
        ROOT.read_raw_image(self.file_name, header_bytes, self.image)

    def draw(self, options="col"):
        canvas_name = self.file_name + "_canvas"
        self.canvas = ROOT.TCanvas(
                canvas_name,
                canvas_name)
        self.image.Draw(options)

if __name__ == '__main__':
    import sys
    file_name = sys.argv[1]
    image = RawImageReader(file_name)
    image.draw()
    raw_input()
