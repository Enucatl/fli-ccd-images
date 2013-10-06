#include "base_image_reader.h"

namespace readimages {

void BaseImageReader::read_file() {
    std::ifstream file(path_.c_str());
    if (not file.is_open())
        return;
    histogram_.SetName(fs::basename(path_).c_str());
    histogram_.SetTitle(fs::basename(path_).c_str());
    int header_bytes = raw_image_tools::process_header(file, image_info_);
    histogram_.SetBins(
            image_info_.rows,
            image_info_.min_x,
            image_info_.max_x,
            image_info_.columns,
            image_info_.min_y,
            image_info_.max_y);
    raw_image_tools::load_histogram(file, header_bytes, histogram_);
    //std::cout << "columns " << image_info_.columns << std::endl;
    //std::cout << "rows " << image_info_.rows << std::endl;
    //std::cout << "min_x " << image_info_.min_x << std::endl;
    //std::cout << "max_x " << image_info_.max_x << std::endl;
    //std::cout << "min_y " << image_info_.min_y << std::endl;
    //std::cout << "max_y " << image_info_.max_y << std::endl;
    //std::cout << "exposure_time " << image_info_.exposure_time << std::endl;
    //std::cout << "exposure_time_measured " << image_info_.exposure_time_measured << std::endl;
    //std::cout << "timestamp " << image_info_.timestamp << std::endl;
    file.close();
}

}
