#include <iostream>

#include <boost/program_options.hpp>
#include <boost/thread.hpp>

#include "TROOT.h"
#include "TApplication.h"

#include "main_frame.h"

namespace po = boost::program_options;

int main(int argc, char **argv) {
    po::options_description desc("Options");
    desc.add_options()
        ("help,h", "produce help message")
        ("f", po::value<std::string>(), "path of file or folder")
        ("divide,d", po::value<std::string>(), "path of file of flat field")
        ;

    po::positional_options_description positional;
    positional.add("f", 1);
    po::variables_map vm;
    po::store(
            po::command_line_parser(argc, argv).options(desc).positional(positional).run(),
            vm);
    po::notify(vm);

    std::string example = "If a folder is passed as an argument, the programme starts in 'watching' mode: it looks for the newest file in the folder and continuously updates the display.\n\n\nEXAMPLE\n./ccdfli_viewer /afs/psi.ch/project/hedpc/raw_data/2013/ccdfli/2013.01.29/S00000-00999/S00013/";

    if (vm.count("help")) {
        std::cout << desc << std::endl;
        std::cout << example << std::endl;
        return 1;
    }
    
    TApplication app("app", &argc, argv);

    if (gROOT->IsBatch()) {
        std::cout << argv[0] << " cannot run in batch mode!" << std::endl;
        return 1;
    }

    readimages::gui::MainFrame viewer(gClient->GetRoot(), 1024, 768);

    //default start empty GUI:
    if (vm.count("f")) {
        std::string folder = vm["f"].as<std::string>();
        //std::cout << folder << std::endl;
        boost::thread main_thread(&readimages::gui::MainFrame::LaunchImageReader, &viewer, folder);
    }
    if (vm.count("divide")) {
        std::string divide_path = vm["divide"].as<std::string>();
        viewer.Divide(divide_path);
    }
    app.Run();
    return 0;
}

