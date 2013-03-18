#ifndef READ_RAW_IMAGE_H
#define READ_RAW_IMAGE_H

#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <iterator>
#include <algorithm>
#include <numeric>
#include <inttypes.h>

#include <boost/filesystem.hpp>
#include <boost/iterator/filter_iterator.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/algorithm/string.hpp> 

#include "TH2.h"

namespace raw_image_tools {

typedef TH2S Image;

template<typename T> 
struct Reader {
    std::istream& operator()(std::istream& is, T& pixel){
        return is.read(reinterpret_cast<char*>(&pixel), sizeof(pixel));
    }
};

struct ImageInfo {
    int rows;
    int columns;
    int min_x;
    int max_x;
    int min_y;
    int max_y;
    double exposure_time;
    double exposure_time_measured;
    long int timestamp;
};

extern const char* kImageInfoDescription;


//load to TH2S the data in file_name, skipping the first header_bytes, as
//they represent the header, already analysed by
//raw_image_tools::process_header
void load_histogram(std::ifstream& file, int header_bytes, Image& image);

//get relevant information from header of raw file: number of rows and
//columns and the range of the axes.
int process_header(std::ifstream& file_name, ImageInfo& image_info);

//check that the file is a valid image file
bool is_image_file(const boost::filesystem::directory_entry& path);

//check if p2 is newer than p1
bool is_file2_newer(const boost::filesystem::path& p1, const boost::filesystem::path& p2);

//watch folder and return the newest of the files in it
void watch_folder(const boost::filesystem::path folder, boost::filesystem::path& new_name);

//get all .raw files in a folder
void get_all_raw_files(const boost::filesystem::path& folder, std::vector<boost::filesystem::path>& vector);

//calculate the ROOT file name corresponding to a folder name given by SPEC
std::string get_root_filename(std::string folder);
}

#endif /* end of include guard: READ_RAW_IMAGE_H */
