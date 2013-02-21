#!/usr/bin/env python                                                                                                                                         
from __future__ import division, print_function                                                                                                               
from progress_bar import progress_bar                                                                                                                         
from subprocess import check_call
import os
import argparse
parser = argparse.ArgumentParser(description='''convert all images to png with the single image reader,
        and save them as GIF with imagemagick convert''')
parser.add_argument('folder', metavar='FOLDER',
        nargs=1, help='folder containing the raw files')

folder = parser.parse_args().folder[0]

#setup program name:
programme = "make_png"

if not os.path.exists(folder) or not os.path.isdir(folder):
    print("Folder not found!", folder)
    print()
    raise OSError

#look for the reader programme in the bin folder
programme_dir = os.listdir("bin")
if programme not in programme_dir:
    programme_dir = os.listdir("../bin")
    if programme not in programme_dir:
        print("Programme not found!", programme)
        print()
        raise OSError
    else:
        programme_dir = "../bin"
else:
    programme_dir = "./bin"

os.environ["PATH"] += ":{0}".format(programme_dir)

command = programme + " {0} -b".format(folder)
check_call(command, shell=True)

gif_creation_command = "convert -delay 50 -loop 1 "
gif_creation_command += os.path.join(folder, "png", "*.png")
gif_name = os.path.join(folder,
        os.path.basename(os.path.normpath(folder)) + ".gif")
gif_creation_command += " " + gif_name
print(gif_creation_command)
check_call(gif_creation_command, shell=True)
