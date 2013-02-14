#include <iostream>
#include <boost/program_options.hpp>

#include "TApplication.h"

#include "read_newest.h"

namespace po = boost::program_options;

int main(int argc, char **argv) {
    po::options_description desc("Options");
    desc.add_options()
        ("help,h", "produce help message")
        ("folder,f", po::value<std::string>(), "looks for most recent file in this folder")
        ;

    po::positional_options_description positional;
    positional.add("folder", 1);
    po::variables_map vm;
    po::store(
            po::command_line_parser(argc, argv).options(desc).positional(positional).run(),
            vm);
    po::notify(vm);

    std::string example = "EXAMPLE\n./online_viewer /afs/psi.ch/project/hedpc/raw_data/2013/ccdfli/2013.01.29/S00000-00999/S00013/";

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

