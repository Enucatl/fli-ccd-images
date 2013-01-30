#include <iostream>
#include <vector>
#include <algorithm>
#include <iterator>
#include <boost/program_options.hpp>
#include <boost/filesystem.hpp>
#include <boost/iterator/filter_iterator.hpp>

#include "TApplication.h"

#include "raw_image_tools.h"
#include "raw_image_reader.h"

namespace po = boost::program_options;
namespace fs = boost::filesystem;

int main(int argc, char **argv) {
    po::options_description desc("Options");
    desc.add_options()
        ("help", "produce help message")
        ("folder", po::value<std::string>(), "looks for most recent file in this folder")
        ;
    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    po::notify(vm);

    std::string example = "./read_newest --folder /home/abis_m/afsproject/raw_data/2013/ccdfli/2013.01.29/S00000-00999/S00013/";

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
    raw_image_tools::RawImageReader image_reader;
    std::vector<fs::path> files;
    fs::path previous_newest;
    app.Run();

    return 0;
}

