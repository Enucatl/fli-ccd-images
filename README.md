# Read and analyse CCD FLI images

## Requirements

[GIT](http://git-scm.com/ "GIT homepage") version control system ≥ 1.7

[Python Distribute](http://pythonhosted.org/distribute/index.html) for
installing the python scripts

[Numpy](http://www.numpy.org/) for calculations

[h5py](http://code.google.com/p/h5py/) storing and reading the images

[skimage](http://scikit-image.org/docs/dev/api/skimage.html) for the
`pitch.py` script.

[TOMCAT's gridrec](https://intranet.psi.ch/Tomcat/SVN-Overview) only for the
tomographic reconstruction


## Report Bugs & Request Features

please report any bug or feature request using the [issues webpage](https://bitbucket.org/Enucatl/readimages/issues/new).


## Download

    :::bash
    git clone https://bitbucket.org/Enucatl/readimages.git

or 

    :::bash
    git clone git@bitbucket.org:Enucatl/readimages.git

## Install

    :::bash
    python setup.py develop


if you do not have root permissions, you can still install it by appending
    the `--user` flag.

## Programmes
Use the `-h` flag to get help.

### View CCDFLI raw files
read a single file

   * `ccdfli_viewer.py`

### Make HDF5 file
reads all images in a folder and convert them from RAW to HDF5.
This file is then used in all the other scripts.

   * `make_hdf5.py`

### X-ray flux analysis

   * `intensity_scan.py`: plot the integral in the image as a function of
      the image number.

### Analyse stacks
The easiest way to reconstruct a 2D image out of 1D lines is to stack the
lines together. More tools are then provided to analyse the stack:

   * `projection_stack.py`: make the stacked image.
   * `export_stack.py`: save the stacked image in a different format
     (default: png).

### Alignment tools

   * `pitch.py`: rotation about the `y` axis.

### Differential phase contrast
The differential phase contrast images can be calculated from phase stepping
scans:

   * `dpc_radiography.py`: reconstruct the absorption, differential phase,
      and visibility reduction images.
   * `phase_drift.py`: show the drift of the phase values during a scan.
   * `visibility_map.py`: draw a graph with the visibility as a function of
      the pixel in the detector.
   * `dpc_scan.py`: reconstruct the scan taken with the [dpc scan SPEC macro](https://bitbucket.org/Enucatl/spec_macros/src/master/dpc_radiography.mac)

### Tomographic reconstruction
Reconstruct a dataset with gridrec.

   * `ct_reconstruction.py`: reconstruct a dataset with gridrec.
