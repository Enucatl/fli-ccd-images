#include "raw_image_reader.h"

namespace fs = boost::filesystem;

namespace readimages {

void SingleImageReader::update_histogram() {
    boost::mutex::scoped_lock lock(mutex_);
    if (not path_)
        file_found_.wait(lock);
    read_file();
    return;
}

void SingleImageReader::set_path(fs::path path) {
    boost::mutex::scoped_lock lock(mutex_);
    if (fs::exists(path)) {
        path_ = path;
        file_found_.notify_one();
    }
    else
        path_ = "";
    return;
}

}
