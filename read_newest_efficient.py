#!/usr/bin/env python2.7
from __future__ import division, print_function
import sys
import os
from time import sleep
from raw_image_reader import RawImageReader, RawImageReaderScikit

import argparse

def get_file_time(filename):
    return os.stat(filename).st_mtime

parser = argparse.ArgumentParser(description='''
        keep looking for newest raw
        file and display it as an image.''')
parser.add_argument('folder', metavar='FOLDER', nargs='?',
        default=".", help='path of the folder where the files are saved')
folder = parser.parse_args().folder

previous_newest = ""
file_list = []
while not previous_newest:
    try:
        if not os.path.exists(folder):
            raise OSError("folder does not exist.")
        file_list = os.listdir(folder)
        "look for .raw files"
        file_list = [os.path.join(folder, file_name)
                for file_name in file_list
                if ".raw" in file_name]
        "continue if no files in directory"
        if not file_list:
            continue
        previous_newest = file_list[0]
        #sleep(0.5)
    except KeyboardInterrupt:
        print()
        print()
        print("Exiting.")
        break

image_reader = RawImageReader(previous_newest)
image_reader.draw()

while True:
    try:
        file_list = os.listdir(folder)
        "look for .raw files"
        file_list = [os.path.join(folder, file_name)
                for file_name in file_list
                if ".raw" in file_name]
        newest = max(file_list, key=get_file_time)
        if newest != previous_newest:
            print("found new file:", newest)
            previous_newest = newest
            image_reader.update(newest)
    except KeyboardInterrupt:
        print()
        print()
        print("Exiting.")
        break
