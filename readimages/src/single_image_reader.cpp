#include "single_image_reader.h"

namespace fs = boost::filesystem;

namespace readimages {

void SingleImageReader::update_histogram() {
    boost::mutex::scoped_lock lock(mutex_);
    file_found_.timed_wait(lock, boost::posix_time::milliseconds(200));
    read_file();
    histogram_drawn_.notify_one();
    return;
}

void SingleImageReader::set_path(fs::path path) {
    boost::mutex::scoped_lock lock(mutex_);
    if (fs::exists(path)) {
        path_ = path;
        //std::cout << "single image reader " << path.string() << std::endl;
        file_found_.notify_one();
    }
    else {
        std::cout << "File not found!" << std::endl;
        path_ = "file.not.found";
    }
    return;
}

}
