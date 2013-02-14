#include "raw_image_reader.h"

namespace readimages {

RawImageReader::RawImageReader(TCanvas* canvas):
    histogram_("image_hist", "image_hist",
            1, 0, 1, 1, 0, 1)
    {
        canvas_ = canvas;
        //contrast adjustment canvas:
}

bool RawImageReader::load_image(std::string file_name) {
    canvas_->SetTitle(boost::filesystem::basename(file_name).c_str());
    if (not boost::filesystem::exists(file_name))
        return false;
    int rows, columns, min_x, min_y, max_x, max_y;
    std::ifstream file(file_name.c_str());
    if (not file.is_open())
        return false;
    int header_bytes = raw_image_tools::process_header(file, rows, columns,
            min_x, min_y, max_x, max_y);
    histogram_.SetBins(rows, min_x, max_x,
            columns, min_y, max_y);
    raw_image_tools::load_histogram(file, header_bytes, histogram_);
    file.close();
    return true;
}

void RawImageReader::draw(const char* options) {
    canvas_->cd();
    histogram_.Draw("col");
}

void RawImageReader::save(std::string file_name) {
    canvas_->SaveAs(file_name.c_str());
}

}
