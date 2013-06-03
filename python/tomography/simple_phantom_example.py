#!/usr/bin/env python
#
# NiftyRec Python Example Program
#
# D. Duke
# Energy Systems Division
# Argonne National Laboratory, Illinois, USA
#
# Supply a phantom via an 8-bit image, project it to a sinogram and then try and reconstruct it using et_project and et_backproject.
# Demonstrates use of the python interface to NiftyRec.
#
# NOTE: This program requires PIL (Python Imaging Library) to load a TIFF file and display it.
#
# Last Update: March 5, 2013.
#
##########################################################################################################################################

# Modules from your Python distribution
from __future__ import division, print_function

import time, sys
import numpy
import matplotlib.pyplot as plt
import h5py

from NiftyRec.NiftyRec import et_project as project
from NiftyRec.NiftyRec import et_list_gpus as list_gpus
from NiftyRec.NiftyRec import et_get_block_size as get_block_size
from Reconstruction import Reconstructor
from simple_phantom_image_handling import *

##########################################################################################################################################
# Configure the settings below appropriately for your system.

verbose=True					# Show additional output while processing.
use_the_GPU=False				# Set to TRUE if you have a CUDA-enabled card and have build NiftyRec to use it.
input_phantom="test.hdf5"			# Source phantom image.
theta0=0 ; theta1=360; n_cameras=721		# Number of equispaced virtual projections of the phantom
method='je'  					# Methods available in Python are osem, tv, je, ccje.
params={'subset_order':8,'steps':30,'beta':0.}	# Parameters that methods may need in NiftyRec.
padFactor=1.0					# How much zero padding around the image as a fraction of image size. Must be >= 1.
resize_display=5				# Zoom the small image when showing it onscreen, so we can see it better.
psf_one=numpy.ones((1,1))			# Unity point spread function

### BEGIN MAIN ###########################################################################################################################

# Start a timer
start_time=time.time()

N = n_cameras

# Create Reconstructor
volume_size = (N, 1, N)
print("The test phantom volume is of size"+str(volume_size))
r = Reconstructor(volume_size)

# Camera angles
r.set_cameras_equispaced(theta0, theta1, n_cameras, axis=1)  # r.cameras is in radians!

# Apply PSF to every view
psf_mat=numpy.zeros((psf_one.shape[0],psf_one.shape[1],N))
for k in range(N): psf_mat[:,:,k]=psf_one
r.set_psf_matrix( psf_mat )
print("The point spread function is of size"+str(psf_mat.shape))

# Check if CUDA is to be used , and show some diagnostic info.
r.set_use_gpu(use_the_GPU)
if use_the_GPU:	CPUGPU='GPU'
else:		CPUGPU='CPU'
print("Using GPU?"+str(r.use_gpu))
if use_the_GPU: print('GPU Info: ', list_gpus())

input_file = h5py.File('S00140.hdf5')
NRsino = input_file['/postprocessing/stack_pixel_510'][:, 100:821]
NRsino = numpy.reshape(NRsino, (NRsino.shape[0], 1, NRsino.shape[1]))
print("Size of NiftyRec\'s sinogram:"+str(NRsino.shape))

# Load sinogram and set callbacks
r.set_sinogram(NRsino)
r.set_callback_status(callback_status_handler)
r.set_callback_updateactivity(callback_updateactivity_handler)

# Check if we're ready to go, else quit.
print("All paremeters set? "+str(r.has_all_parameters())+"\n\n")
if not r.has_all_parameters(): sys.exit(1)

# Begin reconstruction
print( 'Reconstructing using `%s\' method on the %s...' % (method,CPUGPU) )
r.reconstruct(method,params,verbose)  # remove underscore to background-thread

# Waiting loop
time.sleep(1)			# r._reconstructing may not go high immediately.
while r._reconstructing:
	time.sleep(1)		# Don't hammer on the CPU while we wait!
	sys.stdout.flush()

# Stop the clock
elapsed_time = time.time() - start_time

# Make NumPy arrays of the first slice of the volume for the input phantom & reconstruction.
slice_output = r.activity[:, 0, :]
if "reconstruction" in input_file:
    del input_file["reconstruction"]
input_file.create_dataset("reconstruction", data=slice_output)
input_file.close()

# Determine sum square error in the reconstruction of the phantom
print("Time elapsed: %i seconds (on the %s)" % (numpy.ceil(elapsed_time),CPUGPU))

# Display sinogram, output images 
sinogram_slice_imageArray = NRsino[:, 0, :].reshape(r.N_cameras, N)
plt.figure()
plt.imshow(sinogram_slice_imageArray)
plt.figure()
plt.imshow(slice_output)
plt.ion()
plt.show()
raw_input("press ENTER to quit.")


