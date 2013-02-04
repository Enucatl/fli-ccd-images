#include <iostream>

#include "TApplication.h"
#include "TStyle.h"
#include "TCanvas.h"

#include "rootstyle.h"
#include "contrast_adjuster.h"


int main(int argc, const char **argv) {
    TApplication app("app", &argc, argv);
    TStyle* style = setTDRstyle();
    style->cd();
    TCanvas main_canvas("canvas", "canvas");
    TH2D histogram("hist", "hist", 100, -3, 3, 100, -3, 3);
    histogram.FillRandom("gaus", 10000);

    root_style::ContrastAdjuster contrast_adjuster;

    contrast_adjuster.get_intensity_distribution(histogram);
    contrast_adjuster.set_style(style);
    contrast_adjuster.Draw();
    
    return 0;
}


