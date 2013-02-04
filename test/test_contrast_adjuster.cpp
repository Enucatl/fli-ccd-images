#include <iostream>

#include "TApplication.h"
#include "TROOT.h"
#include "TStyle.h"
#include "TCanvas.h"

#include "rootstyle.h"
#include "contrast_adjuster.h"


int main(int argc, char **argv) {
    TApplication app("app", &argc, argv);
    TStyle* style = setTDRStyle();
    style->cd();
    TCanvas main_canvas("canvas", "canvas");
    TH2D histogram("hist", "hist", 100, -1, 1, 1000, -1, 1);
    histogram.FillRandom("gaus", 10000000);
    histogram.Draw("col");

    root_style::ContrastAdjuster contrast_adjuster;

    contrast_adjuster.get_intensity_distribution(histogram);
    contrast_adjuster.set_style(style);
    contrast_adjuster.set_mother_canvas(&main_canvas);
    contrast_adjuster.draw();
    
    //TCanvas main_canvas2("canvas2", "canvas");
    //TH2D histogram2("hist2", "hist", 1000, -2, 2, 1000, -2, 2);
    //histogram2.FillRandom("gaus", 10000000);
    //histogram2.Draw("col");
    app.Run();
    return 0;
}


