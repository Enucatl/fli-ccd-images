from setuptools import setup, find_packages

setup(
    name = "ReadImages",
    version = "3",
    packages = find_packages(),
    scripts = [
        'readimages_utils/export_dataset.py',
        'projections/projection_stack.py',
        'alignment/pitch.py',
        'alignment/roll.py',
        'dpc/dpc_radiography.py',
        'dpc/phase_drift.py',
        'dpc/visibility_map.py',
        'raw_images/make_hdf5.py',
        'raw_images/export_images.py',
        'raw_images/intensity_scan.py',
        'tomography/tomography.py',
        ],

    install_requires = [
        'h5py',
        'numpy',
        'scikit-image'],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
    },

    # metadata for upload to PyPI
    author = "Matteo Abis",
    author_email = "matteo.abis@psi.ch",
    description = "Read and analyse FLI CCD raw images",
    license = "GNU GPL 3",
    keywords = "readimages",
    url = "https://bitbucket.org/Enucatl/readimages",   # project home page, if any
    # could also include long_description, download_url, classifiers, etc.
)
