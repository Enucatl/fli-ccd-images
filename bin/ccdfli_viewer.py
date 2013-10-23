#!/usr/bin/env python
# encoding: utf-8

"""
Display a raw file. If it you pass a directory it watches for updates and always
shows the most recent RAW file in it.

"""

from __future__ import division, print_function

import argparse
import os

import pyinotify
import matplotlib.pyplot as plt
from scipy import stats

from readimages.raw_images.read_raw import read_data
from readimages.print_version import print_version

class EventHandler(pyinotify.ProcessEvent):
    def my_init(self, folder):
        plt.ion()
        self._fig = plt.figure()
        self._ax = self._fig.add_subplot(111)
        file_list = [os.path.join(folder, f)
                for f in os.listdir(folder)
                if f.lower().endswith(".raw")]
        newest = max(file_list,
                key=lambda x: os.stat(x).st_mtime)
        image = read_data(newest)
        self._plt_image = plt.imshow(image, aspect='auto')
        simple_name = os.path.splitext(os.path.basename(newest))[0]
        limits = stats.mstats.mquantiles(image, prob=[0.02, 0.98])
        self._plt_image.set_clim(*limits)
        plt.title(simple_name.replace("_", " "))

    def process_IN_CLOSE_WRITE(self, event):
        if os.path.splitext(event.pathname)[1].lower() != ".raw":
            print(event.pathname, "not a RAW file")
        else:
            image = read_data(event.pathname)
            self._plt_image.set_array(image)
            simple_name = os.path.splitext(os.path.basename(event.pathname))[0]
            limits = stats.mstats.mquantiles(image, prob=[0.02, 0.98])
            self._plt_image.set_clim(*limits)
            plt.title(simple_name.replace("_", " "))
            self._ax.set_xlim(0, image.shape[1] - 1)
            self._ax.set_ylim(0, image.shape[0] - 1)
            self._fig.canvas.draw()

if __name__ == '__main__':
    commandline_parser = argparse.ArgumentParser(__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    commandline_parser.add_argument('f',
            nargs=1,
            help='folder or file to display'
            )
    print_version(commandline_parser.prog)
    args = commandline_parser.parse_args()
    file_name = args.f[0]
    if os.path.isfile(file_name):
        if os.path.splitext(file_name)[1].lower() != ".raw":
            raise IOError("{0} is not a RAW file!".format(file_name))
        simple_name = os.path.splitext(os.path.basename(file_name))[0]
        image = read_data(file_name)
        plt.figure()
        plt.title(simple_name.replace("_", " "))
        plt_image = plt.imshow(image, aspect='auto')
        limits = stats.mstats.mquantiles(image, prob=[0.02, 0.98])
        plt_image.set_clim(*limits)
        plt.ion()
        plt.show()
        raw_input("Press ENTER to close.")
    elif os.path.isdir(file_name):
        try:
            wm = pyinotify.WatchManager()
            handler = EventHandler(folder=file_name)
            mask = pyinotify.IN_CLOSE_WRITE
            notifier = pyinotify.ThreadedNotifier(wm, handler)
            notifier.start()
            watch = wm.add_watch(file_name, mask)
            raw_input("Press ENTER to close.")
        except KeyboardInterrupt:
            print("closing")
        finally:
            notifier.stop()
    elif not os.path.exists(file_name):
        raise OSError("{0} not found!".format(file_name))
    else:
        print(file_name, "exists but is not a file or a directory")
