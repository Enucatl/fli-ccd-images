#include "base_image_reader.h"

namespace readimages {

void BaseImageReader::read_file() {
    std::ifstream file(path_.c_str());
    if (not file.is_open())
        return;
    histogram_.SetName(fs::basename(path_).c_str());
    histogram_.SetTitle(fs::basename(path_).c_str());
    int rows, columns, min_x, min_y, max_x, max_y;
    int header_bytes = raw_image_tools::process_header(file,
            rows, columns,
            min_x, min_y, max_x, max_y);
    histogram_.SetBins(rows, min_x, max_x,
            columns, min_y, max_y);
    raw_image_tools::load_histogram(file, header_bytes, histogram_);
    file.close();
}

}
