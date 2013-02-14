#include <iostream>
#include <fstream>
#include <string>
#include <boost/program_options.hpp>
#include <boost/algorithm/string/replace.hpp>
#include <boost/filesystem.hpp>

#include "TApplication.h"

#include "raw_image_reader.h"

namespace po = boost::program_options;
namespace fs = boost::filesystem;

int main(int argc, char **argv) {
    po::options_description desc("Options");
    desc.add_options()
        ("help,h", "produce help message")
        ("file_name,f", po::value<std::string>(), "file name of frame")
        ("save", "save file as png (default=false)")
        ;
    po::positional_options_description positional;
    positional.add("file_name", 1);
    po::variables_map vm;
    po::store(
            po::command_line_parser(argc, argv).options(desc).positional(positional).allow_unregistered().run(),
            vm);
    po::notify(vm);

    std::string example = "EXAMPLE\n./single_image_reader /afs/psi.ch/project/hedpc/raw_data/2013/ccdfli/2013.01.29/S00000-00999/S00013/ccdimage_00013_00068_00.raw";
    std::string save_example = "\n\n if you also want to save the image as png, use --save";
    example += save_example;

    if (vm.count("help")) {
        std::cout << desc << std::endl;
        std::cout << example << std::endl;
        return 1;
    }

    std::string file_name;
    //default is not to save the png image, but to show it
    bool save = false;

    if (vm.count("file_name")) {
        file_name = vm["file_name"].as<std::string>();
    }
    else{
        std::cout << desc << std::endl;
        std::cout << example << std::endl;
        return 2;
    }
    if (vm.count("save")) {
        save = true;
    }

    TApplication app("app", &argc, argv);
    raw_image_tools::RawImageReader image_reader;
    bool loaded = image_reader.load_image(file_name);
    if (loaded)
        image_reader.draw();
    if (save) {
        //save in separate png folder
        //begin string operations to build the new filename
        fs::path input_name(file_name);
        fs::path input_folder(input_name.parent_path());
        fs::path output_folder = input_folder / fs::path("png");
        fs::create_directories(output_folder);
        fs::path output_name = input_name.filename();
        std::string output_name_string((output_folder / output_name).string());
        std::cout << output_name_string << std::endl;
        boost::algorithm::replace_last(output_name_string, ".raw", ".png");
        //end string operations
        image_reader.save(output_name_string);
    }
    else
        app.Run(); //don't Run when saving output image
    return 0;
}

