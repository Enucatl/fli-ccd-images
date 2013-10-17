from __future__ import division, print_function

import os
import h5py
import numpy as np

from readimages.dpc.image_reconstructor import ImageReconstructor
from readimages.raw_images.base_analyser import post_processing_dirname

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    http://stackoverflow.com/a/312464
    """
    for i in xrange(0, len(l), n):
        yield l[i:i + n]

class ScanReconstructor(object):

    """Reconstruct a scan made with the dpc_scan macro.
    https://bitbucket.org/Enucatl/spec_macros/src/master/dpc_radiography.mac"""

    def __init__(self,
            files,
            pixel,
            roi,
            phase_steps,
            periods,
            flats_every,
            n_flats, 
            extension,
            overwrite):
        """
        :files: list of the hdf5 files containing the single phase stepping
        curves
        :phase_steps: number of steps in the phase stepping curve
        :periods: number of periods scanned
        :flats_every: flats were taken every flats_every steps of the sample
        motor
        :n_flats: n_flats are averaged each time a flat is to be taken
        :extension: format for the output images.

        """
        self._files = files
        self._pixel = pixel
        self._roi = roi
        self._phase_steps = phase_steps
        self._periods = periods
        self._projections = int(len(files) / (1 + n_flats / flats_every))
        self._flats_every = flats_every
        self._n_flats = n_flats
        self._format = extension
        self._overwrite = overwrite
        first_file_name, ext = os.path.splitext(os.path.basename(files[0]))
        last_file_name = os.path.splitext(os.path.basename(files[-1]))[0]
        dir_name = os.path.dirname(files[0])
        self._output_file_name = os.path.join(dir_name, "{0}_{1}{2}".format(
            first_file_name, last_file_name, ext))
        self._export_name = os.path.splitext(
                self._output_file_name)[0] + "." + extension
        if os.path.exists(self._output_file_name) and not overwrite:
            raise OSError("""File {0} exists!
            
            --overwrite to overwrite, aborting.""".format(
                self._output_file_name))
        elif os.path.exists(self._output_file_name) and overwrite: 
            os.remove(self._output_file_name)
        self._output_file = h5py.File(self._output_file_name, "w-")
        self._output_group = self._output_file.create_group(
                post_processing_dirname)
        image_size = (self._projections, roi[1] - roi[0])
        self._absorption_image = self._output_group.create_dataset(
                "absorption",
                image_size, dtype=np.float)
        self._differential_phase_image = self._output_group.create_dataset(
                "differential_phase",
                image_size, dtype=np.float)
        self._dark_field_image = self._output_group.create_dataset(
                "visibility_reduction",
                image_size, dtype=np.float)
        self._absorption_image_title = "absorption"
        self._differential_phase_image_title = "differential phase"
        self._dark_field_image_title = "visibility reduction"

    def reconstruct(self):
        """Perform the reconstruction by stitching together the
        ImageReconstructor output images.

        """
        chunk_size = self._flats_every + self._n_flats
        total_chunks = int(np.ceil(len(self._files) / chunk_size))
        for i, chunk in enumerate(chunks(self._files, chunk_size)):
            print("chunk {0}/{1}".format(i + 1, total_chunks))
            image = chunk[:-self._n_flats]
            flats = chunk[-self._n_flats:]
            reconstructor = ImageReconstructor(image,
                    flats, self._pixel, self._roi,
                    self._phase_steps, self._periods,
                    self._format, self._overwrite)
            reconstructor.calculate_images()
            reconstructor.correct_drift()
            first_pixel = i * self._flats_every
            last_pixel = (i + 1) * self._flats_every
            self._absorption_image[
                    first_pixel:last_pixel, :] = reconstructor.absorption_image
            self._differential_phase_image[
                    first_pixel:last_pixel, :
                    ] = reconstructor.differential_phase_image
            self._dark_field_image[
                    first_pixel:last_pixel, :] = reconstructor.dark_field_image

    def save(self):
        """After closing all datasets will not be accessible!"""
        self._output_file.close()

    def draw(self):
        """Display the calculated images with matplotlib."""
        import matplotlib.pyplot as plt
        from scipy import stats

        _, (ax1, ax2, ax3) = plt.subplots(
                3, 1, sharex=True)
        img1 = ax1.imshow(self._absorption_image,
                cmap=plt.cm.Greys)
        limits = stats.mstats.mquantiles(self._absorption_image,
                prob=[0.02, 0.98])
        img1.set_clim(*limits)
        ax1.axis("off")
        ax1.set_title(self._absorption_image_title)
        img2 = ax2.imshow(self._differential_phase_image)
        limits = stats.mstats.mquantiles(self._differential_phase_image,
                prob=[0.02, 0.98])
        #limits = (-3, 3)
        img2.set_clim(*limits)
        ax2.axis("off")
        ax2.set_title(self._differential_phase_image_title)
        img3 = ax3.imshow(self._dark_field_image)
        ax3.set_title(self._dark_field_image_title)
        ax3.axis("off")
        limits = stats.mstats.mquantiles(self._dark_field_image,
                prob=[0.02, 0.98])
        img3.set_clim(*limits)
        plt.tight_layout()
        if self._absorption_image.shape[0] == 1:
            _, (hist1, hist2, hist3) = plt.subplots(
                    3, 1, sharex=True)
            hist1.hist(range(self._absorption_image.shape[1]),
                    bins=self._absorption_image.shape[1],
                    weights=self._absorption_image.T, fc='w', ec='k')
            hist1.set_title("absorption")
            hist2.hist(range(self._differential_phase_image.shape[1]),
                    bins=self._differential_phase_image.shape[1],
                    weights=self._differential_phase_image.T, fc='w', ec='k')
            hist2.set_title("differential phase")
            hist3.hist(range(self._dark_field_image.shape[1]),
                    bins=self._dark_field_image.shape[1],
                    weights=self._dark_field_image.T, fc='w', ec='k')
            hist3.set_title("visibility reduction")
        #histograms
        #plt.figure()
        #plt.hist(image_array.flatten(), 256,
                #range=(np.amin(image_array),
                    #np.amax(image_array)), fc='w', ec='k')
        #plt.figure()
        #plt.hist(self._dark_field_image.flatten(), 256,
                #range=(np.amin(self._dark_field_image),
                    #np.amax(self._dark_field_image)), fc='k', ec='k')
        #plt.figure()
        #plt.hist(self._differential_phase_image.flatten(), 256,
                #range=(np.amin(self._differential_phase_image),
                    #np.amax(self._differential_phase_image)), fc='k', ec='k')
        #print("mean phase {0:.4f} +- {1:.4f}".format(
                #np.mean(self._differential_phase_image),
                #np.std(self._differential_phase_image) /
                #math.sqrt(roi[1] - roi[0])))
        if not os.path.exists(self._export_name) or self._overwrite:
            plt.savefig(self._export_name)
            print("saved", self._export_name)
        plt.ion()
        plt.show()
        raw_input("Press ENTER to quit.")
