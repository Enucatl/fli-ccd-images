#include "read_newest.h"

namespace raw_image_tools {

ReadNewest::ReadNewest(std::string folder):
    folder_(folder) {
}

void ReadNewest::update_histogram() {
    //never returns!
    while (true){
        boost::mutex::scoped_lock lock(mutex_);
        new_file_found_.wait(lock);
        //std::cout << "received signal " << current_newest_ << std::endl;
        image_reader_.load_image(current_newest_.string());
        image_reader_.draw();
    }
}

void ReadNewest::watch_folder() {
    //never returns!
    std::vector<boost::filesystem::path> files;
    while (true) {
        boost::filesystem::directory_iterator dir_first(folder_), dir_last;
        std::copy(boost::make_filter_iterator(raw_image_tools::is_image_file, dir_first, dir_last),
                boost::make_filter_iterator(raw_image_tools::is_image_file, dir_last, dir_last),
                std::back_inserter(files)
                );
        boost::filesystem::path newest = *std::max_element(files.begin(), files.end(), raw_image_tools::is_file2_newer);
        if (newest == current_newest_) {
            continue;
        }
        else {
            boost::mutex::scoped_lock lock(mutex_);
            current_newest_ = newest;
            //std::cout << current_newest_ << std::endl;
            new_file_found_.notify_one();
        }
    }
}

}
