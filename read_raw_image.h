#ifndef READ_RAW_IMAGE_H
#define READ_RAW_IMAGE_H

#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <iterator>
#include <algorithm>
#include <inttypes.h>
#include "TH2.h"

template<typename T> 
struct Reader {
    std::istream& operator()(std::istream& is, T& pixel){
        return is.read(reinterpret_cast<char*>(&pixel), sizeof(pixel));
    }
};

void read_raw_image(std::string file_name, int header_bytes, TH2& image);
#endif /* end of include guard: READ_RAW_IMAGE_H */
