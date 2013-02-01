#ifndef RAW_IMAGE_READER_H
#define RAW_IMAGE_READER_H

#include <iostream>
#include <fstream>
#include <string>

#include <boost/filesystem.hpp>

#include "TROOT.h"
#include "TStyle.h"
#include "TH2.h"
#include "TCanvas.h"
#include "rootstyle.h"

#include "raw_image_tools.h"

namespace raw_image_tools {

class RawImageReader {
public:
    RawImageReader();
    ~RawImageReader();
    bool load_image(std::string file_name);
    void draw(const char* options="");
    void update();

private:
    bool draw_called_;
    TH2D histogram_;
    TCanvas canvas_;
    TStyle* style_;
};

}

#endif /* end of include guard: RAW_IMAGE_READER_H */
