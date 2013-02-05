#include <iostream>

#include "TApplication.h"
#include "TROOT.h"
#include "TStyle.h"
#include "TCanvas.h"
#include "TRootCanvas.h"

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
    contrast_adjuster.set_parent_canvas(&main_canvas);
    contrast_adjuster.draw();
    
    app.Run();
    return 0;
}


