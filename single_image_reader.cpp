#include <iostream>
#include <fstream>
#include <string>
#include <boost/program_options.hpp>

#include "TApplication.h"

#include "raw_image_reader.h"

namespace po = boost::program_options;

int main(int argc, char **argv) {
    po::options_description desc("Options");
    desc.add_options()
        ("help", "produce help message")
        ("file_name", po::value<std::string>(), "file name of frame")
        ;
    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    po::notify(vm);

    std::string example = "./single_image_reader --file_name /home/abis_m/afsproject/raw_data/2013/ccdfli/2013.01.29/S00000-00999/S00013/ccdimage_00013_00068_00.raw";

    if (vm.count("help")) {
        std::cout << desc << std::endl;
        std::cout << example << std::endl;
        return 1;
    }

    std::string file_name;

    if (vm.count("file_name")) {
        file_name = vm["file_name"].as<std::string>();
    }
    else{
        std::cout << desc << std::endl;
        std::cout << example << std::endl;
        return 2;
    }

    TApplication app("app", &argc, argv);
    raw_image_tools::RawImageReader image_reader;
    bool loaded = image_reader.load_image(file_name);
    if (loaded)
        image_reader.draw();
    app.Run();
    return 0;
}

