#include <iostream>
#include <boost/program_options.hpp>
#include <boost/progress.hpp>

#include "TApplication.h"
#include "TCanvas.h"
#include "TFile.h"

#include "raw_image_tools.h"
#include "single_image_reader.h"
#include "root_image_writer.h"

namespace po = boost::program_options;

int main(int argc, char **argv) {
    po::options_description desc("Options");
    desc.add_options()
        ("help,h", "produce help message")
        ("folder,f", po::value<std::string>(), "convert raw files in this folder to TH2D in a ROOT file")
        ;

    po::positional_options_description positional;
    positional.add("folder", 1);
    po::variables_map vm;
    po::store(
            po::command_line_parser(argc, argv).options(desc).positional(positional).allow_unregistered().run(),
            vm);
    po::notify(vm);

    std::string example = "EXAMPLE\n./bin/make_root test";

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

    //file will not be opened if it already exists: exit with return 3
    std::string root_file_name = raw_image_tools::get_root_filename(folder);
    readimages::SingleImageReader image_reader;
    readimages::RootImageWriter image_writer(root_file_name,
            image_reader.get_image_info_ptr(),
            image_reader.get_histogram_ptr());
    if (image_writer.open_failed()) {
        return 3;
    }

    std::vector<fs::path> files;

    raw_image_tools::get_all_raw_files(folder, files);

    int n = files.size();
    std::cout << std::endl;
    std::cout << "Converting " << n << " RAW files" << std::endl;
    boost::progress_display progress(n);

    for (std::vector<fs::path>::const_iterator file_name = files.begin(); file_name != files.end(); ++file_name) {
        ++progress;
        image_reader.set_path(*file_name);
        image_reader.update_histogram();
        image_writer.Fill();
    }
    std::cout << "Saving ROOT file:" << std::endl;
    std::cout << root_file_name << std::endl;
    image_writer.Write();
    std::cout << "Done!" << std::endl;

    return 0;
}

