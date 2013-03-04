#include <iostream>
#include <boost/program_options.hpp>
#include <boost/filesystem.hpp>

#include "TFile.h"

#include "single_image_reader.h"

namespace po = boost::program_options;
namespace fs = boost::filesystem;

int main(int argc, char **argv) {
    po::options_description desc("Options");
    desc.add_options()
        ("help,h", "produce help message")
        ("file,f", po::value<std::string>(), "convert raw file in this folder to TH2D and add to automatically named ROOT file")
        ;

    po::positional_options_description positional;
    positional.add("file", 1);
    po::variables_map vm;
    po::store(
            po::command_line_parser(argc, argv).options(desc).positional(positional).run(),
            vm);
    po::notify(vm);

    std::string example = "EXAMPLE\n./bin/add_image_to_root_file test/ccdimage_ct_000547.raw\n\n";
    example += "Adds a TH2D called ccdimage_ct_000547 to the file test/test.root (and creates it if it doesn't exist)";

    if (vm.count("help")) {
        std::cout << desc << std::endl;
        std::cout << example << std::endl;
        return 1;
    }

    std::string image_file_name_string;
    if (vm.count("file")) {
        image_file_name_string = vm["file"].as<std::string>();
    }
    else{
        std::cout << desc << std::endl;
        std::cout << example << std::endl;
        return 2;
    }

    fs::path image_file_name(image_file_name_string);
    fs::path output_root_file(image_file_name.parent_path());
    output_root_file /= output_root_file.filename();
    output_root_file.replace_extension(".root");
    std::cout << output_root_file << std::endl;
    TFile root_file(output_root_file.string().c_str(), "update");
    readimages::SingleImageReader image_reader;
    image_reader.set_path(image_file_name);
    image_reader.update_histogram();
    image_reader.Write();
    root_file.Close();
    return 0;
}
