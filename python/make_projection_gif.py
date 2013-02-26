#!/usr/bin/env python                                                                                                                                         
from __future__ import division, print_function                                                                                                               
from progress_bar import progress_bar                                                                                                                         
from subprocess import check_call
import os
import argparse
import tempfile
import shutil

parser = argparse.ArgumentParser(description='''save GIF with projection
        along pixel PIXEL''')
parser.add_argument('file', metavar='FILE',
        nargs=1, help='ROOT file with the RAW images converted to TH2D')
parser.add_argument('pixel', metavar='PIXELS',
        nargs='+', help='pixel number(s)')

root_file_name = parser.parse_args().file[0]
pixel = parser.parse_args().pixel

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

ROOT.gROOT.SetBatch(True)
canvas = ROOT.TCanvas("canvas", "canvas")

#check pixel command line arg
if len(pixel) == 1:
    pixel.append(pixel[0])
elif len(pixel) > 2:
    print("only two pixels (begin and end) can be specified!")
    raise OSError

pixel = [int(x) for x in pixel]


canvas.cd()
print("creating temp folder... ", end="")
tmp_folder_name = tempfile.mkdtemp()
print(tmp_folder_name)

for key in list_of_keys:
    name = key.GetName()
    obj = key.ReadObj()
    if not obj.InheritsFrom("TH2"):
        continue
    first_pixel = int(obj.GetYaxis().GetBinLowEdge(1))
    projection = obj.ProjectionX("_px", pixel[0] - first_pixel, pixel[1] -
            first_pixel)
    projection.SetTitle(name + " pixel " + str(pixel[0]))
    projection.Draw()
    output_name = os.path.join(tmp_folder_name, name + ".png")
    canvas.SaveAs(output_name)

gif_creation_command = "convert -delay 50 -loop 1 "
gif_creation_command += os.path.join(tmp_folder_name, "*.png")
gif_name = root_file_name.replace(".root", "_projections.gif")
gif_creation_command += " " + gif_name
print(gif_creation_command)
check_call(gif_creation_command, shell=True)

print("removing temp folder... ", end="")
print(tmp_folder_name)
shutil.rmtree(tmp_folder_name)

print()
print("generated gif file with the projections:")
print(gif_name)
