# ccdfli viewer

ROOT GUI programme to view the files recorded by the CCD
FLI camera in OFLG/U210.


## Requirements

[GCC](gcc.gnu.org "GCC homepage") ≥ 4.3 for move semantics used with boost::thread

[GNU make](www.gnu.org/software/make/ "make homepage") ≥ 3.80 for order-only prerequisites with '|' in this Makefile

The [BOOST c++ libraries](http://www.boost.org "BOOST homepage") ≥ 1.50

The [ROOT data analysis framework](http://root.cern.ch "ROOT homepage") ≥ 5.34

[GIT](http://git-scm.com/ "GIT homepage") version control system ≥ 1.7

[Python Distribute](http://pythonhosted.org/distribute/index.html) for
installing the python scripts


## Report Bugs & Request Features

please report any bug or feature request using the [issues webpage](https://bitbucket.org/Enucatl/readimages/issues/new).


## Download

    :::bash
    git clone https://bitbucket.org/Enucatl/readimages.git

    or 

    :::bash
    git clone git@bitbucket.org:Enucatl/readimages.git

## Compile

    :::bash
    make


if the compiler cannot find the proper headers and libraries, you are
    probably missing these variables (ready to copy & paste on a bash shell
    on `mpc1054.psi.ch`):

    :::bash
    #setup ROOT from afs/cern.ch
    source /afs/cern.ch/sw/lcg/external/gcc/4.6/x86_64-slc6-gcc46-opt/setup.sh
    source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.03/x86_64-slc6-gcc46-opt/root/bin/thisroot.sh
    alias root='root -l'
    #setup boost c++ libraries
    #change the following line if needed
    #so that it points to your installation of Boost
    export BOOST_HOME=/home/specuser/boost_install
    export CPLUS_INCLUDE_PATH=${BOOST_HOME}/include:$CPLUS_INCLUDE_PATH
    export LD_LIBRARY_PATH=${BOOST_HOME}/lib:$LD_LIBRARY_PATH
    export LIBRARY_PATH=${BOOST_HOME}/lib:$LIBRARY_PATH
    export PATH=~/.local/bin:$LIBRARY_PATH


## Run

run the programme by supplying a FILE or FOLDER name on the command line

    :::bash
    ./bin/ccdfli_viewer FILE/FOLDER

if you specify a FOLDER name, it will continuously update the display with
    the most recent image in the folder.


## Post-processing and other bonus programmes

The python scripts will be installed with the `python setup.py --user` option, and will end up in `~/.local/bin`. This folder should therefore be appended to the `PATH` variable.

### Make ROOT file
reads all images in a folder and convert them from RAW to TH2D in a ROOT file.
This ROOT file format is used in all the other scripts.

    :::bash
    ./bin/make_root FOLDER

### Analyse the raw images
Three scripts are provided to apply the same operation to each raw image
(saved in the ROOT format):

    * `correct.py`: subtract a dark, divide by a flat and append the results
      to the input file.
    * `export_images.py`: save all images in another format (gif, png...).
    * `intensity_scan.py`: plot the integral in the image as a function of
      the image number.

### Analyse stacks
The easiest way to reconstruct a 2D image out of 1D lines is to stack the
lines together. More tools are then provided to analyse the stack:

    * `projection_stack.py`: make the stacked image.
    * `export_stack.py`: save the stacked image in a different format.

### Alignment tools
The stacked images can yield interesting alignment information:

    * `roll.py`: rotation about the `x` axis.
    * `pitch.py`: rotation about the `y` axis.

### Differential phase contrast
The differential phase contrast images can be calculated from phase stepping
scans:

    * `dpc_radiography.py`: reconstruct the absorption, differential phase,
      and visibility reduction images.
    * `phase_drift.py`: show the drift of the phase values during a scan.
    * `visibility_map.py`: draw a graph with the visibility as a function of
      the pixel in the detector.
