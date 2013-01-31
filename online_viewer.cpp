#include <iostream>
#include <boost/program_options.hpp>

#include "TApplication.h"

#include "read_newest.h"

namespace po = boost::program_options;

int main(int argc, char **argv) {
    po::options_description desc("Options");
    desc.add_options()
        ("help", "produce help message")
        ("folder", po::value<std::string>(), "looks for most recent file in this folder")
        ;
    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    po::notify(vm);

    std::string example = "./online_viewer --folder /afs/psi.ch/project/hedpc/raw_data/2013/ccdfli/2013.01.29/S00000-00999/S00013/";

    if (vm.count("help")) {
        std::cout << desc << std::endl;
        std::cout << example << std::endl;
        return 1;
    }

    std::string folder;

    if (vm.count("folder")) {
        folder = vm["folder"].as<std::string>();
    }
    else{
        std::cout << desc << std::endl;
        std::cout << example << std::endl;
        return 2;
    }

    TApplication app("app", &argc, argv);
    raw_image_tools::ReadNewest read_newest(folder);
    boost::thread folder_lookup_thread(&raw_image_tools::ReadNewest::watch_folder, &read_newest);
    boost::thread update_histogram_thread(&raw_image_tools::ReadNewest::update_histogram, &read_newest);
    app.Run();
    return 0;
}

