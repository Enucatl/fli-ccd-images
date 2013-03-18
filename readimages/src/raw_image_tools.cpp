#include "raw_image_tools.h"

namespace raw_image_tools {

const char* kImageInfoDescription = "rows/I:columns:min_x:max_x:min_y:max_y:exposure_time/D:exposure_time_measured:timestamp/L";

void load_histogram(std::ifstream& file, int header_bytes, Image& image) {
    //get size of image
    int columns = image.GetNbinsX();
    int rows = image.GetNbinsY();
    int number_of_pixels = columns * rows;
    std::vector<short> temp_vector(number_of_pixels, 0);
    file.seekg(header_bytes);
    file.read(reinterpret_cast<char*>(&temp_vector[0]), number_of_pixels * sizeof(uint16_t));
    //fix total integral
    image.SetEntries(number_of_pixels);

    //set transposed data:
    for (int u = 0; u < rows; u++) {
        for (int v = 0; v < columns; v++) {
            image.fArray[columns + 2 + u * (columns + 2) + v + 1] = temp_vector[u + rows * v];
        }
    }
}

int process_header(std::ifstream& file, ImageInfo& image_info) {
    Reader<char> reader;
    char value;
    int header_byte_counter = 0;
    std::string line;
    std::vector<std::string> split_line;
    split_line.reserve(8);
    bool end_of_header_reached = false;
    while(reader(file, value) and not end_of_header_reached){
        header_byte_counter++;
        line.push_back(value);
        if (value == '\n') { 
            //std::cout << line;
            if (boost::algorithm::contains(line, "rows")) {
                boost::algorithm::split(split_line, line, boost::algorithm::is_space());
                image_info.rows = boost::lexical_cast<int>(split_line.at(2));
            }
            else if (boost::algorithm::contains(line, "columns")) {
                boost::algorithm::split(split_line, line, boost::algorithm::is_space());
                image_info.columns = boost::lexical_cast<int>(split_line.at(2));
            }
            else if (boost::algorithm::contains(line, "exptimesec_client")) {
                boost::algorithm::split(split_line, line, boost::algorithm::is_space());
                image_info.exposure_time = boost::lexical_cast<double>(split_line.at(2));
            }
            else if (boost::algorithm::contains(line, "exptimesec_measured")) {
                boost::algorithm::split(split_line, line, boost::algorithm::is_space());
                image_info.exposure_time_measured = boost::lexical_cast<double>(split_line.at(2));
            }
            else if (boost::algorithm::contains(line, "ROI")) {
                boost::algorithm::split(split_line, line, boost::algorithm::is_space());
                image_info.min_y = boost::lexical_cast<int>(split_line.at(2));
                image_info.min_x = boost::lexical_cast<int>(split_line.at(3));
                image_info.max_y = boost::lexical_cast<int>(split_line.at(4));
                image_info.max_x = boost::lexical_cast<int>(split_line.at(5));
            }
            else if (boost::algorithm::contains(line, "timestamp_integer")) {
                boost::algorithm::split(split_line, line, boost::algorithm::is_space());
                image_info.timestamp = boost::lexical_cast<long int>(split_line.at(2));
            }
            else if (boost::algorithm::contains(line, "EOH")) {
                header_byte_counter++;
                end_of_header_reached = true;
            }
            line.erase();
        }
    }
    //std::cout << "columns " << image_info.columns << std::endl;
    //std::cout << "rows " << image_info.rows << std::endl;
    //std::cout << "min_x " << image_info.min_x << std::endl;
    //std::cout << "max_x " << image_info.max_x << std::endl;
    //std::cout << "min_y " << image_info.min_y << std::endl;
    //std::cout << "max_y " << image_info.max_y << std::endl;
    //std::cout << "exposure_time " << image_info.exposure_time << std::endl;
    //std::cout << "exposure_time_measured " << image_info.exposure_time_measured << std::endl;
    //std::cout << "timestamp " << image_info.timestamp << std::endl;
    return header_byte_counter;
}

bool is_image_file(const boost::filesystem::directory_entry& path){
    //check if a file is a raw image file
    return boost::filesystem::is_regular_file(path) and path.path().extension().string() == ".raw";
}

bool is_file2_newer(const boost::filesystem::path& p1, const boost::filesystem::path& p2){
    return boost::filesystem::last_write_time(p1) < boost::filesystem::last_write_time(p2);
}

void get_all_raw_files(const boost::filesystem::path& folder, std::vector<boost::filesystem::path>& vector){
    //folder MUST exist already, otherwise throws an exception
    boost::filesystem::directory_iterator dir_first(folder), dir_last;
    std::copy(boost::make_filter_iterator(raw_image_tools::is_image_file, dir_first, dir_last),
            boost::make_filter_iterator(raw_image_tools::is_image_file, dir_last, dir_last),
            std::back_inserter(vector)
            );
}

std::string get_root_filename(std::string folder){
    if (*folder.rbegin() == '/')
        //if last character is / erase it
        folder.erase(folder.begin() + folder.size() - 1);
    return folder + ".root";
}

}
