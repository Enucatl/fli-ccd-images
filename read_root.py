#!/usr/bin/env python
from __future__ import division, print_function
from rootstyle import tdrstyle_grayscale
import sys
import ROOT

file_name = sys.argv[1]

ROOT.gROOT.ProcessLine(".L read_raw_image.C+")
tdrstyle_grayscale()

input_file = open(file_name, "rb")
text = input_file.read()
input_file.close()
text = text.split("\n")
print(len(text), "lines")
rows = 0
columns = 0
min_x = 0
min_y = 0
max_x = 0
max_y = 0

total_header_lines = 0
for i, line in enumerate(text):
    print(line)
    total_header_lines += 1
    if "rows" in line:
        rows = int(line.split()[2])
    elif "columns" in line:
        columns = int(line.split()[2])
    elif "ROI" in line:
        min_x, min_y, max_x, max_y = (int(x)
                for x in line.split()[2:])
    elif "EOH" in line:
        break

header_bytes = len("".join(text[:total_header_lines])) + 1

print(rows, columns, min_x, min_y, max_x, max_y)
image = ROOT.TH2I(file_name, file_name,
        rows,
        min_x,
        max_x,
        columns,
        min_y,
        max_y)
ROOT.read_raw_image(file_name, header_bytes, image)

image.Draw("col")
raw_input()
