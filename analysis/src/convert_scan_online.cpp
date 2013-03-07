#include <iostream>
#include <string>
#include <boost/program_options.hpp>
#include <boost/filesystem.hpp>

#include "TFile.h"

#include "raw_image_tools.h"
#include "single_image_reader.h"

namespace po = boost::program_options;
namespace fs = boost::filesystem;

int main(int argc, char **argv) {
    po::options_description desc("Options");
    desc.add_options()
        ("help,h", "produce help message")
        ("folder,f", po::value<std::string>(), "name of the folder where the images are saved")
        ;

    po::positional_options_description positional;
    positional.add("folder", 1);
    po::variables_map vm;
    po::store(
            po::command_line_parser(argc, argv).options(desc).positional(positional).run(),
            vm);
    po::notify(vm);

    std::string example = "EXAMPLE\n./bin/convert_scan_online test\n\n";
    example += "convert raw images to TH2 format as they are saved to the disk. The programme waits for you to supply the file names from stdin as the images are taken. This should be automated from python with subprocess.Popen.communicate().";

    if (vm.count("help")) {
        std::cout << desc << std::endl;
        std::cout << example << std::endl;
        return 1;
    }

    std::string folder;
    if (vm.count("folder")) {
        folder = vm["folder"].as<std::string>();
        if (not fs::is_directory(folder))
            return 2;
    }
    else{
        std::cout << desc << std::endl;
        std::cout << example << std::endl;
        return 3;
    }

    std::string root_file_name = raw_image_tools::get_root_filename(folder);
    std::cout << root_file_name << std::endl;
    TFile root_file(root_file_name.c_str(), "create");
    if (not root_file.IsOpen()) {
        std::cout << "ROOT file already exists or failed to open, exiting:" << std::endl;
        std::cout << root_file_name << std::endl;
        return 4;
    }
    readimages::SingleImageReader image_reader;
    std::string image_file_name;
    std::cout << "next image file_name:" << std::endl;
    while(std::cin >> image_file_name) {
        std::cout << image_file_name << std::endl;
        if (not raw_image_tools::is_image_file(
                    fs::directory_entry(image_file_name))) {
            break;
        }
        image_reader.set_path(image_file_name);
        image_reader.update_histogram();
        image_reader.Write();
        std::cout << "next image file_name:" << std::endl;
    }
    root_file.Close();
    return 0;
}
