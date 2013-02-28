#!/usr/bin/env python                                                                                                                                         
from __future__ import division, print_function                                                                                                               
from progress_bar import progress_bar                                                                                                                         
from subprocess import check_call
import os
import argparse
import array

parser = argparse.ArgumentParser(description='''save GIF with projection
        along pixel PIXEL''')
parser.add_argument('file', metavar='FILE.root',
        nargs=1, help='ROOT file with the RAW images converted to TH2D')
parser.add_argument('--roi', metavar=('min_x', 'max_x', 'min_y', 'max_y'),
        nargs=4, help='min_x max_x min_y max_y')

root_file_name = parser.parse_args().file[0]
roi = parser.parse_args().roi

#setup program name:
if not os.path.exists(root_file_name):
    print("File not found!", root_file_name)
    print()
    raise OSError


import ROOT

root_file = ROOT.TFile(root_file_name)
list_of_keys = root_file.GetListOfKeys()
next_item = ROOT.TIter(list_of_keys)
key = next_item.next()
obj = key.ReadObj()
while not obj.InheritsFrom("TH2"):
    key = next_item.next()
    obj = key.ReadObj()


roi = [int(x) for x in roi]
x_min, x_max, y_min, y_max = roi
x1 = obj.GetXaxis().FindFixBin(x_min)
x2 = obj.GetXaxis().FindFixBin(x_max)
y1 = obj.GetYaxis().FindFixBin(y_min)
y2 = obj.GetYaxis().FindFixBin(y_max)

x = []
y = []

for i, key in enumerate(list_of_keys):
    name = key.GetName()
    obj = key.ReadObj()
    if not obj.InheritsFrom("TH2"):
        continue
    integral = obj.Integral(x1, x2, y1, y2)
    x.append(i + 1)
    y.append(integral)

canvas = ROOT.TCanvas("canvas", "canvas")
n = len(x)
x = array.array("d", x)
y = array.array("d", y)
graph = ROOT.TGraph(n, x, y)
title = "intensity in roi {0[0]}-{0[1]} x {0[2]}-{0[3]};\
file number;\
intensity (integral)".format(roi)
graph.SetName("intensity_graph")
graph.SetMarkerStyle(20)
graph.Draw("ap")
raw_input()
