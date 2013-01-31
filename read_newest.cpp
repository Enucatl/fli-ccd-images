#include "TApplication.h"

#include "read_newest.h"

namespace po = boost::program_options;

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

int main(int argc, char **argv) {
    po::options_description desc("Options");
    desc.add_options()
        ("help", "produce help message")
        ("folder", po::value<std::string>(), "looks for most recent file in this folder")
        ;
    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    po::notify(vm);

    std::string example = "./read_newest --folder /home/abis_m/afsproject/raw_data/2013/ccdfli/2013.01.29/S00000-00999/S00013/";

    if (vm.count("help")) {
        std::cout << desc << std::endl;
        std::cout << example << std::endl;
        return 1;
    }

    std::string folder;

    if (vm.count("folder")) {
        folder = vm["folder"].as<std::string>();
    }
    else{
        std::cout << desc << std::endl;
        std::cout << example << std::endl;
        return 2;
    }

    TApplication app("app", &argc, argv);
    raw_image_tools::ReadNewest read_newest(folder);
    boost::thread folder_lookup_thread(&raw_image_tools::ReadNewest::watch_folder, &read_newest);
    boost::thread update_histogram_thread(&raw_image_tools::ReadNewest::update_histogram, &read_newest);
    app.Run();
    return 0;
}

