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

#include "raw_image_tools.h"

namespace readimages {

class RawImageReader {
public:
    RawImageReader(TCanvas* canvas);
    bool load_image(std::string file_name);
    void draw(const char* options="");
    void update();
    void save(std::string file_name);

private:
    bool draw_called_;
    TH2D histogram_;
    TCanvas* canvas_;
};

}

#endif /* end of include guard: RAW_IMAGE_READER_H */
