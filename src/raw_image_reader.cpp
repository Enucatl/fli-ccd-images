#include "raw_image_reader.h"

namespace raw_image_tools {

RawImageReader::RawImageReader():
    histogram_("image_hist", "image_hist",
            1, 0, 1, 1, 0, 1),
    canvas_("image_canvas", "image_canvas")
    {
        draw_called_ = false;
        canvas_.SetWindowSize(1000, 800);
        style_ = setTDRStyle();
        gROOT->SetStyle("tdrStyle");
        gROOT->ForceStyle();
        canvas_.Update();

        //contrast adjustment canvas:
        contrast_adjuster_.set_style(style_);
        contrast_adjuster_.set_parent_canvas(&canvas_);

}

RawImageReader::~RawImageReader(){
    delete style_;
}

bool RawImageReader::load_image(std::string file_name) {
    canvas_.SetTitle(boost::filesystem::basename(file_name).c_str());
    if (not boost::filesystem::exists(file_name))
        return false;
    int rows, columns, min_x, min_y, max_x, max_y;
    std::ifstream file(file_name.c_str());
    if (not file.is_open())
        return false;
    int header_bytes = process_header(file, rows, columns,
            min_x, min_y, max_x, max_y);
    histogram_.SetBins(rows, min_x, max_x,
            columns, min_y, max_y);
    load_histogram(file, header_bytes, histogram_);
    file.close();
    //setup for contrast adjustment
    contrast_adjuster_.get_intensity_distribution(histogram_);
    return true;
}

void RawImageReader::draw(const char* options) {
    canvas_.cd();
    histogram_.Draw("col");
    canvas_.Update();
    contrast_adjuster_.Draw();
}

void RawImageReader::save(std::string file_name) {
    canvas_.SaveAs(file_name.c_str());
}

}
