#include "contrast_adjuster.h"

namespace root_style {

ContrastAdjuster::ContrastAdjuster():
    n_bins_(100),
    canvas_("contrast_canvas", "contrast_canvas", 200, 400),
    histogram_pad_("contrast_hist_pad", "contrast_hist_pad",
            0.02, 0.1, 0.98, 0.98),
    histogram_("contrast_hist", "contrast_hist",
            n_bins_, 0, 100),
    slider_("slider", "intensity", 
            0.02, 0.02, 0.98, 0.08) {
        canvas_.cd();
        histogram_pad_.Draw();
        slider_.SetObject(this);
}

void ContrastAdjuster::get_intensity_distribution(const TH2& parent_histogram) {
    int n_bins_x = parent_histogram.GetNbinsX();
    int n_bins_y = parent_histogram.GetNbinsY();
    int total_bins = n_bins_x * n_bins_y;
    double minimum_value = parent_histogram.GetMinimum();
    double maximum_value = parent_histogram.GetMaximum();
    histogram_.Reset();
    histogram_.SetBins(n_bins_, minimum_value, maximum_value);
    for (int i = 0; i < total_bins; i++) {
        double value = parent_histogram.GetBinContent(i + 1);
        histogram_.Fill(value);
    }
}

void ContrastAdjuster::draw(const char* options) {
    histogram_pad_.cd();
    histogram_.Draw();
}

void ContrastAdjuster::update_style() {
    //see: http://ultrahigh.org/2007/08/making-pretty-root-color-palettes/
    //on how to make such a colour palette
    const int NRGBs = 5;
    const int NCont = 999;
    std::cout << "updated style" << std::endl;

    //get slide values
    double white = slider_.GetMaximum();
    double black = slider_.GetMinimum();

    //define stops, see:
    //http://root.cern.ch/root/html/TColor.html#TColor:CreateGradientColorTable
    double interval = white - black;
    double colour0 = black;
    double colour1 = 0.34 * interval + black;
    double colour2 = 0.61 * interval + black;
    double colour3 = 0.84 * interval + black;
    double colour4 = white;

    double red[NRGBs]   = { 0.00, 0.34, 0.61, 0.84, 1.00 };
    double green[NRGBs] = { 0.00, 0.34, 0.61, 0.84, 1.00 };
    double blue[NRGBs]  = { 0.00, 0.34, 0.61, 0.84, 1.00 };
    double stops[NRGBs] = { colour0, colour1, colour2, colour3, colour4 };
    std::cout << colour0 << " " << colour4 << std::endl;
    TColor::CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont);
    style_->SetNumberContours(NCont);
    style_->cd();
    mother_canvas_->Update();
    mother_canvas_->Update();
}

void ContrastAdjuster::ExecuteEvent(int event, int px, int py) {
    //only do something on mouse1 down or up
    if (event == 1 or event == 11)
        update_style();
    else
        return;
}

}
