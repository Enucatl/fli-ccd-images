//calculates the integral of a certain region in every picture inside a
//folder.
//Plots and saves the resulting graph
//
#include <iostream>
#include <vector>
#include <sstream>

#include <boost/filesystem.hpp>
#include <boost/program_options.hpp>
#include <boost/progress.hpp>

#include "TApplication.h"
#include "TCanvas.h"
#include "TROOT.h"
#include "TStyle.h"
#include "TGraph.h"

#include "raw_image_tools.h"
#include "single_image_reader.h"
#include "rootstyle.h"

namespace po = boost::program_options;
namespace fs = boost::filesystem;

int main(int argc, char **argv) {
    po::options_description desc("Options");
    desc.add_options()
        ("help,h", "produce help message")
        ("folder,f", po::value<std::string>(), "plot graph with integral of intensity in a region of interest for all files in this folder")
        ;

    po::options_description roi_config("ROI config");
    roi_config.add_options()
        ("roi", po::value< std::vector<int> >()->multitoken()->composing(), "x_min,x_max,y_min,y_max")
        ;

    po::options_description command_line_options;
    command_line_options.add(desc).add(roi_config);

    po::positional_options_description positional;
    positional.add("folder", 1);

    po::variables_map vm;
    po::store(
            po::command_line_parser(argc, argv).options(command_line_options).positional(positional).allow_unregistered().run(),
            vm);
    po::notify(vm);


    const char* config_file_name = "intensity_scan.config";
    if (fs::exists(config_file_name)) {
        vm.clear();
        std::ifstream config_file(config_file_name);
        po::store(
                po::parse_config_file(config_file, roi_config),
                vm);
        po::notify(vm);
    }

    std::string example = "EXAMPLE\n./intensity_scan /afs/psi.ch/project/hedpc/raw_data/2013/ccdfli/2013.01.29/S00000-00999/S00013/ --roi 1 100 1 100";

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

    std::vector<int> roi;

    if (vm.count("roi")) {
        roi = vm["roi"].as< std::vector <int> >();
        if (roi.size() < 4) {
            std::cout << desc << std::endl;
            std::cout << example << std::endl;
            return 3;
        }
    }
    else{
        std::cout << desc << std::endl;
        std::cout << example << std::endl;
        return 3;
    }

    TApplication app("app", &argc, argv);

    int x_min = roi.at(0);
    int x_max = roi.at(1);
    int y_min = roi.at(2);
    int y_max = roi.at(3);

    readimages::SingleImageReader image_reader;
    std::vector<fs::path> files;

    raw_image_tools::get_all_raw_files(folder, files);

    //TCanvas canvas("canvas", "canvas", 1400, 1400);

    //save in separate png folder
    //begin string operations to build the new filename
    fs::path output_folder = folder / fs::path("png");
    fs::create_directories(output_folder);

    TStyle style = setTDRStyle();
    gROOT->SetStyle("tdrStyle");
    gROOT->ForceStyle();

    int n = files.size();
    std::cout << std::endl;
    std::cout << "Analyzing " << n << " RAW files" << std::endl;
    boost::progress_display progress(n);

    std::vector<double> x;
    std::vector<double> y;

    for (int i = 0; i < n; i++) {
        ++progress;
        image_reader.set_path(files[i]);
        image_reader.update_histogram();
        const TH2D& hist = image_reader.get_histogram();
        //convert to bin numbers
        int x1 = hist.GetXaxis()->FindFixBin(x_min);
        int x2 = hist.GetXaxis()->FindFixBin(x_max);
        int y1 = hist.GetYaxis()->FindFixBin(y_min);
        int y2 = hist.GetYaxis()->FindFixBin(y_max);
        double integral = hist.Integral(x1, x2, y1, y2);
        x.push_back(i + 1);
        y.push_back(integral);
    }

    TCanvas intensity_canvas;
    TGraph intensity_graph(n, &x[0], &y[0]);

    std::stringstream title;
    title << "intensity in roi " << x_min << "-"
        << x_max << " x " << y_min << "-" << y_max;
    title << ";file number;intensity (integral)";
    intensity_graph.SetTitle(title.str().c_str());
    intensity_graph.GetXaxis()->SetNdivisions(n);
    intensity_graph.Draw("ap");
    std::cout << "Done!" << std::endl;

    app.Run();
    return 0;
}

