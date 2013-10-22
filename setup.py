#pylint: disable=C0111

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
from version import get_git_version

setup(
    name = "ReadImages",
    version = get_git_version(),
    packages = find_packages(),
    scripts = [
        'bin/ccdfli_viewer.py',
        'bin/export_dataset.py',
        'bin/projection_stack.py',
        'bin/pitch.py',
        'bin/dpc_radiography.py',
        'bin/phase_drift.py',
        'bin/visibility_map.py',
        'bin/make_hdf5.py',
        'bin/export_images.py',
        'bin/intensity_scan.py',
        'bin/ct_reconstruction.py',
        'bin/dpc_scan.py',
        ],

    install_requires = [
        'h5py',
        'numpy',
        'pyinotify',
        'scipy',
        'scikit-image'],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
    },

    # metadata for upload to PyPI
    author = "Matteo Abis",
    author_email = "matteo.dot.abis.at@.psi.ch",
    description = "Read and analyse FLI CCD raw images",
    license = "GNU GPL 3",
    keywords = "readimages",
    # project home page, if any
    url = "https://bitbucket.org/Enucatl/readimages",
    # could also include long_description, download_url, classifiers, etc.
)
