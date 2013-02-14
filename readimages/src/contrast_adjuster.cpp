#include "contrast_adjuster.h"

namespace readimages {

ContrastAdjuster::ContrastAdjuster():
    n_bins_(100),
    histogram_pad_("contrast_hist_pad", "contrast_hist_pad",
            0.02, 0.1, 0.98, 0.98),
    histogram_("contrast_hist", "contrast_hist",
            n_bins_, 0, 100),
    slider_("slider", "intensity", 
            0.02, 0.02, 0.98, 0.08),
    parent_canvas_is_set_(false),
    my_canvas_is_set_(false) {
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

void ContrastAdjuster::set_parent_canvas(TCanvas* canvas) {
    parent_canvas_ = canvas;
    parent_canvas_is_set_ = true;
}

void ContrastAdjuster::set_my_canvas(TCanvas* canvas) {
    my_canvas_ = canvas;
    my_canvas_->cd();
    histogram_pad_.Draw();
    my_canvas_is_set_ = true;
}

void ContrastAdjuster::Draw(const char* options) {
    if (not my_canvas_is_set_){
        std::cerr << "ContrastAdjuster::my_canvas_ is not set!" << std::endl;
        std::cerr << "Please call ContrastAdjuster::set_my_canvas(TCanvas* canvas)" << std::endl;
        return;
    }
    histogram_pad_.cd();
    histogram_.Draw();
}

void ContrastAdjuster::update_style() {
    //see: http://ultrahigh.org/2007/08/making-pretty-root-color-palettes/
    //on how to make such a colour palette
    const int NRGBs = 4;
    const int NCont = 100;

    //get slide values
    double white = slider_.GetMaximum();
    double black = slider_.GetMinimum();

    //define stops, see:
    //http://root.cern.ch/root/html/TColor.html#TColor:CreateGradientColorTable

    double red[NRGBs]   = { 0.0, 0.0, 1.0, 1.00 };
    double green[NRGBs] = { 0.00, 0.0, 1.0, 1.00 };
    double blue[NRGBs]  = { 0.00, 0.0, 1.0, 1.00 };
    double stops[NRGBs] = { 0.00, black, white, 1.00 };
    TColor::CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont);
    style_->SetNumberContours(NCont);
    style_->cd();
    parent_canvas_->Modified();
    parent_canvas_->Update();
    std::cout << "black = " << black << "; white = " << white << std::endl;
}

void ContrastAdjuster::ExecuteEvent(int event, int px, int py) {
    if (not parent_canvas_is_set_) {
        std::cerr << "ContrastAdjuster::parent_canvas_ is not set!" << std::endl;
        std::cerr << "Please call ContrastAdjuster::set_parent_canvas(TCanvas* canvas)" << std::endl;
        return;
    }
    //only do something on mouse1 down or up
    if (event == 1 or event == 11)
        update_style();
    else
        return;
}

}
