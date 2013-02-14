#include <iostream>
#include <vector>
#include <algorithm>
#include <iterator>
#include <boost/filesystem.hpp>
#include <boost/iterator/filter_iterator.hpp>
#include <boost/thread.hpp>

#include "TCanvas.h"

#include "raw_image_tools.h"
#include "raw_image_reader.h"

#ifndef READ_NEWEST_H
#define READ_NEWEST_H

namespace fs = boost::filesystem;

namespace readimages {

class ReadNewest {
public:
    ReadNewest(std::string folder, TCanvas* canvas);
    void update_histogram();
    void watch_folder();

private:
    boost::mutex mutex_;
    boost::condition_variable new_file_found_;
    fs::path current_newest_; //this variable is to be shared by the two threads
    fs::path folder_;
    readimages::RawImageReader image_reader_;
};

}

#endif /* end of include guard: READ_NEWEST_H */
