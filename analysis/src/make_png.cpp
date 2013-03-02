#include <iostream>
#include <boost/program_options.hpp>
#include <boost/progress.hpp>

#include "TApplication.h"
#include "TCanvas.h"
#include "TROOT.h"
#include "TStyle.h"

#include "raw_image_tools.h"
#include "single_image_reader.h"
#include "rootstyle.h"

namespace po = boost::program_options;

int main(int argc, char **argv) {
    po::options_description desc("Options");
    desc.add_options()
        ("help,h", "produce help message")
        ("folder,f", po::value<std::string>(), "convert raw files in this folder to png")
        ;

    po::positional_options_description positional;
    positional.add("folder", 1);
    po::variables_map vm;
    po::store(
            po::command_line_parser(argc, argv).options(desc).positional(positional).allow_unregistered().run(),
            vm);
    po::notify(vm);

    std::string example = "EXAMPLE\n./bin/make_png test";

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

    readimages::SingleImageReader image_reader;
    std::vector<fs::path> files;

    raw_image_tools::get_all_raw_files(folder, files);

    TCanvas canvas("canvas", "canvas", 1000, 1000);

    //save in separate png folder
    //begin string operations to build the new filename
    fs::path output_folder = folder / fs::path("png");
    fs::create_directories(output_folder);

    TStyle style = setTDRStyle();
    gROOT->SetStyle("tdrStyle");
    gROOT->ForceStyle();

    int n = files.size();
    std::cout << std::endl;
    std::cout << "Converting " << n << " RAW files" << std::endl;
    boost::progress_display progress(n);

    for (std::vector<fs::path>::const_iterator file_name = files.begin(); file_name != files.end(); ++file_name) {
        ++progress;
        image_reader.set_path(*file_name);
        image_reader.update_histogram();
        image_reader.Draw("col");
        //begin string operations for the file name
        fs::path output_name = file_name->filename();
        std::string output_name_string((output_folder / output_name).string());
        boost::algorithm::replace_last(output_name_string, ".raw", ".png");
        //end string operations
        canvas.SaveAs(output_name_string.c_str());
    }

    std::cout << "Done!" << std::endl;

    return 0;
}

