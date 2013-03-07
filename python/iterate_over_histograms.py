#!/usr/bin/env python
from __future__ import division, print_function
import os

import ROOT

from cache_values import memoize_method

class HistogramIterator(object):
    """
    Iterator over the TH1 (and daughter types) objects contained in a ROOT file,
    that is passed to the constructor of the iterator"""

    def __init__(self, root_file_name):
        super(HistogramIterator, self).__init__()
        if not os.path.exists(root_file_name):
            raise IOError("File not found", root_file_name)
        self.root_file = ROOT.TFile(root_file_name)
        self.list_of_keys = self.root_file.GetListOfKeys()
        self.root_iter = ROOT.TIter(self.list_of_keys)
        
    def __iter__(self):
        return self

    def next(self):
        key = self.root_iter.next()
        obj = key.ReadObj()
        if obj.InheritsFrom("TH1"):
            return obj
        else:
            self.next()

    def __getitem__(self, index):
        if isinstance(index, (int, long)):
            key = self.list_of_keys.At(index)
            if not key:
                "got null pointer"
                raise IndexError("index {0} out of range of HistogramIterator!".format(index))
            obj = key.ReadObj()
            while not obj.InheritsFrom("TH1"):
                index += 1
                return self.__getitem__(index)
            return obj
        else:
            raise TypeError("key for HistogramIterator must be an integer")

    @memoize_method("length")
    def __len__(self):
        length = 0
        for item in self.list_of_keys:
            if item.ReadObj().InheritsFrom("TH1"):
                length += 1
        return length

if __name__ == '__main__':
    """test"""
    root_file_name = "test/test.root"
    histograms = HistogramIterator(root_file_name)
    print(len(histograms))
    print(histograms[1])
    print(histograms[0])
    try:
        "this should be out of range"
        print(histograms[2])
    except IndexError, e:
        print(e)
    for histogram in histograms:
        print(histogram, histogram.Integral())
    "next should print the cached length"
    print(len(histograms))
