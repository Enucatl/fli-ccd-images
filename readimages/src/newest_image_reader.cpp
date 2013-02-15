#include "newest_image_reader.h"

namespace readimages {

void NewestImageReader::update_histogram() {
    //never returns!
    while (true){
        boost::mutex::scoped_lock lock(mutex_);
        new_file_found_.wait(lock);
        read_file();
    }
}

void NewestImageReader::set_path(fs::path path) {
    while (not boost::filesystem::exists(path)) {
        //wait if folder not found
        std::cerr << "Folder " << path <<
            " not found! I will wait for half a second..." << std::endl;
        boost::this_thread::sleep(boost::posix_time::milliseconds(500));
    }
    std::vector<boost::filesystem::path> files;
    while (true) {
        raw_image_tools::get_all_raw_files(path, files);
        if (not files.size()) {
        std::cerr << "Folder " << path <<
            " empty! I will wait for half a second..." << std::endl;
            //wait if no files found
            boost::this_thread::sleep(boost::posix_time::milliseconds(500));
            continue;
        }
        boost::filesystem::path newest = *std::max_element(files.begin(), files.end(), raw_image_tools::is_file2_newer);
        if (newest == path_) {
            boost::this_thread::sleep(boost::posix_time::milliseconds(100));
            continue;
        }
        else {
            boost::mutex::scoped_lock lock(mutex_);
            path_ = newest;
            new_file_found_.notify_one();
        }
    }
}

}
