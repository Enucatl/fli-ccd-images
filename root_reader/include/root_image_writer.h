#ifndef ROOT_IMAGE_WRITER_H_N5ZEQAGR
#define ROOT_IMAGE_WRITER_H_N5ZEQAGR

#include <iostream>
#include "TFile.h"
#include "TTree.h"
#include "TBranch.h"

#include "raw_image_tools.h"

namespace readimages {

class RootImageWriter {

public:
    RootImageWriter(const std::string root_output_name,
            raw_image_tools::ImageInfo* image_info,
            raw_image_tools::Image* image);
    bool open_failed() const { return open_failed_; }
    void print_current();
    int Fill() { return tree_.Fill(); }
    int Write() { return tree_.Write(); }
    void Close() { root_file_.Close(); }


private:
    bool open_failed_;
    TFile root_file_;
    TTree tree_;
};

}
#endif /* end of include guard: ROOT_IMAGE_WRITER_H_N5ZEQAGR */

