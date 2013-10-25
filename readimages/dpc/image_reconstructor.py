"""Reconstruct the three signals from images and flats."""

from __future__ import division, print_function

import os

import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

from readimages.raw_images.base_analyser import post_processing_dirname
from readimages.utils.progress_bar import progress_bar
import readimages.utils.rcparams #pylint: disable=W0611
from readimages.utils.hadd import hadd
from readimages.dpc.phase_stepping_utils import get_signals
from readimages.dpc.phase_stepping_utils import subtract_drift
from readimages.projections.get_projection_stack import get_projection_stack

class ImageReconstructor(object):
    """Reconstruct the three signals from the phase stepping curve of the
    grating interferometer.
    
    """

    def __init__(self, image_files,
            flat_files,
            pixel,
            roi,
            steps, periods,
            extension,
            overwrite):
        self.overwrite = overwrite
        self.image_array = get_projection_stack(image_files, pixel, 
                roi, overwrite)
        self.flat_image = get_projection_stack(flat_files, pixel,
                roi, overwrite)
        open_option = "a"
        self.input_file = h5py.File(hadd(image_files), open_option)
        output_names = self.set_names()
        self.output_directory = self.input_file.require_group(
                post_processing_dirname)
        self.export_name = hadd(image_files).replace("hdf5", extension)
        self.n_steps = steps
        self.n_periods = periods
        self.n_flats = self.flat_image.shape[0] // self.n_steps
        self.extension = extension
        #Overwrite if necessary
        if self.overwrite:
            self.exists_in_file = False
            for name in output_names:
                if name in self.output_directory:
                    del self.output_directory[name]
            self.initialize_reconstruction()
        else:
            images = {}
            for name in output_names:
                if name in self.output_directory:
                    images[name] = self.output_directory[name]
            if len(images) == 3:
                #All three images were saved, don't recalculate them
                self.absorption_image = self.output_directory[
                        self.absorption_image_name]
                self.differential_phase_image = self.output_directory[
                        self.differential_phase_image_name]
                self.dark_field_image = self.output_directory[
                        self.dark_field_image_name]
                self.exists_in_file = True
            else:
                self.exists_in_file = False
                self.initialize_reconstruction()

    def initialize_reconstruction(self):
        """Calculate the flat parameters and properly stack the images in a
        3D structure so that the phase steps are along axis=2.

        """
        #Average flats if more than one flat image.
        flat_images = np.dstack(np.split(self.flat_image,
            self.n_flats, axis=0))
        #rows and columns have to be swapped with rollaxis so that
        #the image is displayed properly
        flat_images = np.rollaxis(flat_images, 2, 1)
        flat_absorption, flat_phase, flat_dark_field = get_signals(
                    flat_images,
                    None, self.n_periods)
        unwrapped_phase = np.unwrap(flat_phase, axis=0)
        if self.n_flats > 1:
            corrected_flat_phase = subtract_drift(unwrapped_phase)
        else:
            corrected_flat_phase = unwrapped_phase
        average_absorption = np.median(flat_absorption, axis=0)
        average_phase = np.median(corrected_flat_phase, axis=0)
        average_dark_field = np.median(flat_dark_field, axis=0)
        self.flat_parameters = (average_absorption,
                average_phase,
                average_dark_field)
        self.n_lines = self.image_array.shape[0] // self.n_steps 
        if self.image_array.shape[0] % self.n_steps:
            raise ValueError("""
            wrong number of steps,
            division does not result in an integer.
            Image shape: {0}""".format(self.image_array.shape))
        self.images = np.dstack(np.split(
            self.image_array, self.n_lines, axis=0))
        self.images = np.rollaxis(self.images, 2, 1)

    def set_names(self):
        """Set the titles of the images."""
        self.absorption_image_title = "absorption"
        self.differential_phase_image_title = "differential phase"
        self.dark_field_image_title = "visibility reduction"
        self.absorption_image_name = self.absorption_image_title.replace(
                " ", "_")
        self.differential_phase_image_name = self.differential_phase_image_title.replace(
                " ", "_")
        self.dark_field_image_name = self.dark_field_image_title.replace(
                " ", "_")
        output_names = (self.absorption_image_name,
                self.differential_phase_image_name,
                self.dark_field_image_name)
        return output_names

    def calculate_images(self):
        """Calculate the three signals from the phase stepping curves and
        the flat parameters with the get_signals utility function.

        """
        if not self.exists_in_file:
            images = get_signals( 
                self.images,
                self.flat_parameters,
                self.n_periods)
            self.absorption_image, self.differential_phase_image, self.dark_field_image = images
        else:
            print("dpc_radiography: result already saved in file.")
            print(progress_bar(1))


    def save_images(self):
        """Save results to the HDF5 file in the post_processing_dirname
        group.

        """
        if not self.exists_in_file:
            images = self.absorption_image, self.differential_phase_image, self.dark_field_image
            for name, image in zip(self.set_names(), images):
                self.output_directory.create_dataset(
                        name,
                        data=image)
            self.input_file.close()

    def draw(self):
        """Display the calculated images with matplotlib."""
        _, (ax1, ax2, ax3) = plt.subplots(
                3, 1, sharex=True)
        img1 = ax1.imshow(self.absorption_image,
                cmap=plt.cm.Greys)
        limits = stats.mstats.mquantiles(self.absorption_image,
                prob=[0.02, 0.98])
        img1.set_clim(*limits)
        ax1.axis("off")
        ax1.set_title(self.absorption_image_title)
        img2 = ax2.imshow(self.differential_phase_image)
        limits = stats.mstats.mquantiles(self.differential_phase_image,
                prob=[0.02, 0.98])
        #limits = (-3, 3)
        img2.set_clim(*limits)
        ax2.axis("off")
        ax2.set_title(self.differential_phase_image_title)
        img3 = ax3.imshow(self.dark_field_image)
        ax3.set_title(self.dark_field_image_title)
        ax3.axis("off")
        limits = stats.mstats.mquantiles(self.dark_field_image,
                prob=[0.02, 0.98])
        img3.set_clim(*limits)
        plt.tight_layout()
        if self.absorption_image.shape[0] == 1:
            _, (hist1, hist2, hist3) = plt.subplots(
                    3, 1, sharex=True)
            hist1.hist(range(self.absorption_image.shape[1]),
                    bins=self.absorption_image.shape[1],
                    weights=self.absorption_image.T, fc='w', ec='k')
            hist1.set_title("absorption")
            hist2.hist(range(self.differential_phase_image.shape[1]),
                    bins=self.differential_phase_image.shape[1],
                    weights=self.differential_phase_image.T, fc='w', ec='k')
            hist2.set_title("differential phase")
            hist3.hist(range(self.dark_field_image.shape[1]),
                    bins=self.dark_field_image.shape[1],
                    weights=self.dark_field_image.T, fc='w', ec='k')
            hist3.set_title("visibility reduction")
        #histograms
        #plt.figure()
        #plt.hist(image_array.flatten(), 256,
                #range=(np.amin(image_array),
                    #np.amax(image_array)), fc='w', ec='k')
        #plt.figure()
        #plt.hist(self.dark_field_image.flatten(), 256,
                #range=(np.amin(self.dark_field_image),
                    #np.amax(self.dark_field_image)), fc='k', ec='k')
        #plt.figure()
        #plt.hist(self.differential_phase_image.flatten(), 256,
                #range=(np.amin(self.differential_phase_image),
                    #np.amax(self.differential_phase_image)), fc='k', ec='k')
        #print("mean phase {0:.4f} +- {1:.4f}".format(
                #np.mean(self.differential_phase_image),
                #np.std(self.differential_phase_image) /
                #math.sqrt(roi[1] - roi[0])))
        if not os.path.exists(self.export_name) or self.overwrite:
            plt.savefig(self.export_name)
            print("saved", self.export_name)
        plt.ion()
        plt.show()
        raw_input("Press ENTER to quit.")

    def correct_drift(self):
        """Correct the phase image for a phase drift with the subtract_drift
        function.

        """
        self.differential_phase_image_title += " (drift corrected)"
        self.differential_phase_image = subtract_drift(
                self.differential_phase_image)
        
