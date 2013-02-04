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
programme = "single_image_reader"

if not os.path.exists(folder) or not os.path.isdir(folder):
    print("Folder not found!", folder)
    print()
    raise OSError

files = os.listdir(folder)
files = [file_name for file_name in files
        if ".raw" in file_name]

#look for the reader programme in this folder or in the parent folder:
programme_dir = os.listdir(".")
if programme not in programme_dir:
    programme_dir = os.listdir("..")
    if programme not in programme_dir:
        print("Programme not found!", programme)
        print()
        raise OSError
    else:
        programme_dir = ".."
else:
    programme_dir = "."

os.environ["PATH"] += ":{0}".format(programme_dir)

n = len(files)
png_files = []
for i, file_name in enumerate(files):
    file_name = os.path.join(folder, file_name)
    command = programme + " -f {0} --save -b".format(file_name)
    png_files.append(file_name.replace(".raw", ".png"))
    print(progress_bar(i / n), end="")
    check_call(command, shell=True)

gif_creation_command = "convert -delay 50 -loop 1 "
gif_creation_command += os.path.join(folder, "*.png")
gif_name = os.path.join(folder,
        os.path.basename(os.path.normpath(folder)) + ".gif")
gif_creation_command += " " + gif_name
print(gif_creation_command)
check_call(gif_creation_command, shell=True)
