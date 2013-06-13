#!/usr/bin/env python

"""Base class for all the analysers of the images saved in the same HDF5
file.

"""

from __future__ import division, print_function

import warnings
import os

import h5py

from readimages_utils.progress_bar import progress_bar
from readimages_utils.hadd import hadd

#save results of calculations in this group inside the hdf5 file
post_processing_dirname = "postprocessing"
corrected_images_group = "corrected_images"
raw_images_group = "raw_images"

class BaseHDF5Analyser(object):
    """Base class that performs the same operation over all the images in
    the same hdf5 file.
    
    Check if the desired output already exists. By default this is read and
    returned, but it can be optionally recalculated and overwritten
    (overwrite argument).
    
    Setup (open) and cleanup (close) functions are provided, as well as an
    easy loop over all the images."""

    def __init__(self, file_names,
            open_option="r+",
            use_corrected=False,
            overwrite=False,
            batch=False):
        super(BaseHDF5Analyser, self).__init__()
        file_name = hadd(file_names)
        if not os.path.exists(file_name):
            print("File not found", file_name)
            raise IOError
        self.overwrite = overwrite
        self.batch = batch
        self.input_file = h5py.File(file_name, open_option)
        if use_corrected:
            if corrected_images_group in self.input_file:
                self.images = self.input_file[corrected_images_group]
            else:
                warnings.warn("""
                Could not find corrected images!
                Using the raw ones.""")
                self.images = self.input_file[raw_images_group]
        else:
            self.images = self.input_file[raw_images_group]
        self.output_directory = self.input_file.require_group(
                post_processing_dirname)
        self.n_images = len(self.images)
        if self.overwrite and self.output_name() in self.output_directory:
            del self.output_directory[self.output_name()]
        
    @property
    def output_name(self):
        """get name of output object"""
        return "NotImplemented"

    def if_not_exists(self):
        """Hook for some initialization if output object
        was not found in the input file.
        
        """
        self.output_object = 0
        self.exists_in_file = False

    def if_exists(self):
        """Hook for some initialization if output object
        was  found in the input file.
        
        """
        self.dont_start()
        self.exists_in_file = True

    def dont_start(self):
        """Hook for doing some operation when no calculation has to be
        performed.

        """
        print("base_analyser: result already saved in file.")
        print(progress_bar(1))

    def output_exists(self, name):
        """Hook if the output is found in the file."""
        try:
            self.output_object = self.output_directory[self.output_name()]
            return True
        except KeyError:
            return False

    def open(self):
        """Look if the output object already exists and call the appropriate
        methods.

        """
        name = self.output_name()
        if self.overwrite or not self.output_exists(name):
            self.if_not_exists()
        else:
            self.if_exists()

    def __enter__(self):
        self.open()
        return self

    def close(self):
        """write output object if it did not exist and close file"""
        if not self.exists_in_file:
            self.output_directory.create_dataset(
                    self.output_name(),
                    data=self.output_object)
        print()
        print("Done!")
        print()
        self.input_file.close()

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            import traceback
            print(exc_type, exc_value, traceback.print_tb(tb),
                    sep="\n")
        self.close()

    def analyse_histogram(self, i, hist):
        """base version just prints the progress bar advancement for
        the index i"""
        print(progress_bar((i + 1) / self.n_images), end='')

if __name__ == '__main__':
    from raw_images.commandline_parser import commandline_parser
    args = commandline_parser.parse_args()
    file_name = args.file
    overwrite = args.overwrite
    use_corrected = args.corrected
    open_option = "a"
    with BaseHDF5Analyser(file_name,
            open_option,
            use_corrected,
            overwrite) as base_analyser:
        for i, image in enumerate(base_analyser.images):
            base_analyser.analyse_histogram(i, image)
