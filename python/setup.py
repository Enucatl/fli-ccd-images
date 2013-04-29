from setuptools import setup, find_packages

setup(
    name = "ReadImages",
    version = "2.61",
    packages = find_packages(),
    scripts = ['projections/projection_stack.py',
        'projections/export_stack.py',
        'alignment/pitch.py', 'alignment/roll.py',
        'dpc/dpc_radiography.py',
        'dpc/phase_drift.py',
        'dpc/visibility_map.py',
        'raw_images/correct.py',
        'raw_images/export_images.py',
        'raw_images/intensity_scan.py'],

    install_requires = ['numpy',
        'scikit-image'],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
    },

    # metadata for upload to PyPI
    author = "Matteo Abis",
    author_email = "matteo.abis@psi.ch",
    description = "This is an Example Package",
    license = "GNU GPL 3",
    keywords = "readimages",
    url = "https://bitbucket.org/Enucatl/readimages",   # project home page, if any
    # could also include long_description, download_url, classifiers, etc.
)
