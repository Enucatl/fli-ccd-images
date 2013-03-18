#include "root_image_writer.h"

namespace readimages {

RootImageWriter::RootImageWriter(const std::string root_output_name,
        raw_image_tools::ImageInfo* image_info,
        raw_image_tools::Image* image):
    open_failed_(false),
    root_file_(root_output_name.c_str(), "create"),
    tree_("root_image_tree", "root_image_tree") {
    if (not root_file_.IsOpen()) {
        std::cerr << "RootImageWriter::RootImageWriter:\nROOT file already exists or failed to open!" << std::endl;
        std::cerr << root_output_name << std::endl;
        open_failed_ = true;
    }
    else {
        tree_.Branch("image_info", image_info, raw_image_tools::kImageInfoDescription);
        tree_.Branch("image", image);
    }
}

}
