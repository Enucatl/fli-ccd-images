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
}

RawImageReader::~RawImageReader(){
    delete style_;
}

bool RawImageReader::load_image(std::string file_name) {
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
    return true;
}

void RawImageReader::draw(const char* options) {
    draw_called_ = true;
    canvas_.cd();
    histogram_.Draw("col");
    canvas_.Update();
}

void RawImageReader::update() {
    if (draw_called_)
        canvas_.Update();
    else 
        draw();
}

}
