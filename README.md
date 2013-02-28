# ccdfli viewer

ROOT GUI programme to view the files recorded by the CCD
FLI camera in OFLG/U210.

version tags ≥ v2.00 mark the development of the newer (but less stable) GUI app.
If you want the stable versions stick with v1.XX.

To back up to e.g. v1.23 just type `git checkout v1.23`


## Requirements

[GCC](gcc.gnu.org "GCC homepage") ≥ 4.3 (for move semantics used with boost::thread)

[GNU make](www.gnu.org/software/make/ "make homepage") ≥ 3.80 (for order-only prerequisites with '|' in this Makefile)

The [BOOST c++ libraries](http://www.boost.org "BOOST homepage") ≥ 1.50

The [ROOT data analysis framework](http://root.cern.ch "ROOT homepage") ≥ 5.34

[GIT](http://git-scm.com/ "GIT homepage") version control system ≥ 1.7


## Report Bugs & Request Features

please report any bug or feature request using the [issues webpage](https://bitbucket.org/Enucatl/readimages/issues/new).


## Download

    :::bash
    git clone https://bitbucket.org/Enucatl/readimages.git


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
    export CPLUS_INCLUDE_PATH=$(BOOST_HOME)/include:$CPLUS_INCLUDE_PATH
    export LD_LIBRARY_PATH=$(BOOST_HOME)/lib:$LD_LIBRARY_PATH
    export LIBRARY_PATH=$(BOOST_HOME)/lib:$LIBRARY_PATH


## Run

run the programme by supplying a FILE or FOLDER name on the command line

    :::bash
    ./bin/ccdfli_viewer FILE/FOLDER

if you specify a FOLDER name, it will continuously update the display with
    the most recent image in the folder.


## Post-processing and other bonus programmes

### Make PNG, ROOT and GIF files
reads all images in a folder and convert them from RAW to PNG
also saves a gif animation with all the png images and a ROOT file saving
the same images as TH2D

    :::bash
    python python/make_gif.py FOLDER

### Changes of intensity with time
see intensity changes across all the images in a folder (e.g. a scan) in 
a region of interest

    :::bash
    ./bin/intensity_scan ~/afsproject/raw_data/2013/ccdfli/2013.02.22/S00000-00999/S00014/ --roi 250 950 524 531

### GIF of profile along a pixel
see the evolution of a profile in a folder along a pixel. Needs the ROOT
file with all the RAW images inside created by `python/make_gif.py`!

    :::bash
    python python/make_projection_gif.py ROOT_FILE