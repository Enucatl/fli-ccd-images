#!/usr/bin/env python2.7
from __future__ import division, print_function
import sys
import os
from time import sleep
from raw_image_reader import RawImageReader, RawImageReaderScikit

try:
    import argparse
    parser = argparse.ArgumentParser(description='''
            keep looking for newest raw
            file and display it as an image.''')
    parser.add_argument('folder', metavar='FOLDER', nargs='?',
            default=".", help='path of the folder where the files are saved')
    folder = parser.parse_args().folder
except ImportError:
    print("""WARNING: requires argparse from python 2.7 in order to be able to
            specify the folder correctly""")
    try:
        folder = sys.argv[1]
    except IndexError:
        folder = "."

previous_newest = ""
while True:
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
            sleep(2)
            continue
        newest = max(file_list, key=lambda x: os.stat(x).st_mtime)
        if newest != previous_newest:
            print("found new file:", newest)
            previous_newest = newest
            image = RawImageReader(newest)
            image.draw()
        #sleep(0.5)
    except KeyboardInterrupt:
        print()
        print()
        print("Exiting.")
        break



