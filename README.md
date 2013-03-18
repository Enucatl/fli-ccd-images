# ccdfli viewer

ROOT GUI programme to view the files recorded by the CCD
FLI camera in OFLG/U210.


## Requirements

[GCC](gcc.gnu.org "GCC homepage") ≥ 4.3 (for move semantics used with boost::thread)

[GNU make](www.gnu.org/software/make/ "make homepage") ≥ 3.80 (for order-only prerequisites with '|' in this Makefile)

The [BOOST c++ libraries](http://www.boost.org "BOOST homepage") ≥ 1.50

The [ROOT data analysis framework](http://root.cern.ch "ROOT homepage") ≥ 5.34

[GIT](http://git-scm.com/ "GIT homepage") version control system ≥ 1.7

[Pexpect](http://www.noah.org/wiki/pexpect) for the image converting server


## Report Bugs & Request Features

please report any bug or feature request using the [issues webpage](https://bitbucket.org/Enucatl/readimages/issues/new).


## Download

    :::bash
    git clone git@bitbucket.org:Enucatl/readimages.git

or

    :::bash
    git clone https://bitbucket.org/Enucatl/readimages.git

## Compile

    :::bash
    make
    make install


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


## Run

run the programme by supplying a FILE or FOLDER name on the command line

    :::bash
    ./bin/ccdfli_viewer FILE/FOLDER

if you specify a FOLDER name, it will continuously update the display with
    the most recent image in the folder.


## Post-processing and other bonus programmes

### Make ROOT file
reads all images in a folder and convert them from RAW to TH2D in a ROOT file 

    :::bash
    ./bin/make_root FOLDER

### Abstract iterator class:
Inherit from `BaseRootfileAnalyser` in `python/base_rootfile_analyser.py` to
easily perform the same operation on all the images in the ROOT file saved
by `bin/make_root`.

### Convert to images (the default format is GIF)
reads all images in a folder and convert them from RAW to an image format
Needs the ROOT file with all the RAW images inside created by `bin/make_root`!

    :::bash
    python python/convert_images.py FILE.root --format FORMAT

### Changes of intensity with time
see intensity changes across all the images in a folder (e.g. a scan) in 
a region of interest.
Needs the ROOT file with all the RAW images inside created by `bin/make_root`!

    :::bash
    python python/intensity_scan.py FILE.root --roi min_x max_x min_y max_y

### GIF of profile along a pixel
see the evolution of a profile in a folder along a pixel.
Needs the ROOT file with all the RAW images inside created by `bin/make_root`!

    :::bash
    python python/make_projection_gif.py FILE.root

### Draw stack of slices along a pixel
see the evolution of a pixel line by stacking all the slices together.
Needs the ROOT file with all the RAW images inside created by `bin/make_root`!

    :::bash
    python python/make_projection_stack.py FILE.root PIXEL
