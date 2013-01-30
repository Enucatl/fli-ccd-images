#ifndef READ_RAW_IMAGE_H
#define READ_RAW_IMAGE_H

#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <iterator>
#include <algorithm>
#include <inttypes.h>

#include <boost/filesystem.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/algorithm/string.hpp> 

#include "TH2.h"

namespace raw_image_tools {

template<typename T> 
struct Reader {
    std::istream& operator()(std::istream& is, T& pixel){
        return is.read(reinterpret_cast<char*>(&pixel), sizeof(pixel));
    }
};

void load_histogram(std::ifstream& file_name, int header_bytes, TH2& image);
int process_header(std::ifstream& file_name, int& rows, int& columns, int& min_x, int& min_y, int& max_x, int& max_y);
bool is_image_file(const boost::filesystem::directory_entry& path);
bool is_file2_newer(const boost::filesystem::path& p1, const boost::filesystem::path& p2);
void watch_folder(const boost::filesystem::path folder, boost::filesystem::path& new_name);
}

#endif /* end of include guard: READ_RAW_IMAGE_H */
