#include <iostream>
#include <fstream>
#include <boost/program_options.hpp>
#include <boost/filesystem.hpp>

#include "TCanvas.h"
#include "TH2.h"
#include "TApplication.h"
#include "TStyle.h"
#include "TROOT.h"

#include "raw_image_tools.h"

namespace po = boost::program_options;
namespace fs = boost::filesystem;

int main(int argc, char **argv) {
    std::string image_file_name_string;
    int rows = 0;
    int columns = 0;
    int min_x = 0;
    int max_x = 1;
    int min_y = 0;
    int max_y = 1;
    TH2S histogram_short("S", "S",
            columns, min_x, max_x,
            rows, min_y, max_y);
    TH2D histogram_double("D", "D",
            columns, min_x, max_x,
            rows, min_y, max_y);

    while (std::cin >> image_file_name_string) {
        ifstream file(image_file_name_string.c_str());
        ifstream file_short(image_file_name_string.c_str());
        int header_bytes = raw_image_tools::process_header(file, rows, columns, min_x, min_y, max_x, max_y);
        histogram_double.SetBins(rows, min_x, max_x,
                columns, min_y, max_y);
        histogram_short.SetBins(rows, min_x, max_x,
                columns, min_y, max_y);

        raw_image_tools::load_histogram(file, header_bytes, histogram_double);
        raw_image_tools::load_histogram_short(file_short, header_bytes, histogram_short);
    }

    int length_farray = histogram_double.fN;
    std::vector<bool> are_equal(length_farray, false);
    int differences = 0;
    for (int i = 0; i < length_farray; i++) {
        are_equal[i] = histogram_double.fArray[i] == histogram_short[i];
        if (not are_equal[i]) {
            differences++;
            std::cout << i << " " << histogram_double.fArray[i] << " " << histogram_short.fArray[i] << std::endl;
        }
    }
    std::cout << "differences " << differences << "/" << length_farray << std::endl;
    //TApplication app("app", &argc, argv);
    //gStyle->SetPalette(52);
    //gROOT->ForceStyle();
    //TCanvas canvas_short("canvas_short", "canvas_short");
    //histogram_short.Draw("col");
    //TCanvas canvas_double("canvas_double", "canvas_double");
    //histogram_double.Draw("col");
    //app.Run();
    return 0;
}

