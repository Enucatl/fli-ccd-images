#include "raw_image_tools.h"

namespace raw_image_tools {

void load_histogram(std::ifstream& file, int header_bytes, TH2& image) {
    //get size of image
    int columns = image.GetNbinsX();
    int rows = image.GetNbinsY();
    //skip header bytes
    file.seekg(header_bytes);
    Reader<uint16_t> reader;
    uint16_t value = 0;
    int i = 1;
    int j = 0;
    //load the values into the histogram
    while(reader(file, value)) {
        if (j < rows)
            j++;
        else {
            j = 1;
            if (i < columns) i++;
            else i = 1;
        }
        //std::cout << value << std::endl;
        image.SetBinContent(i, j, value);
    }
}

void load_histogram_short(std::ifstream& file, int header_bytes, TH2S& image) {
    //get size of image
    short* matrix = image.fArray;
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
            matrix[columns + 2 + u * (columns + 2) + v + 1] = temp_vector[u + rows * v];
        }
    }
}

int process_header(std::ifstream& file, int& rows, int& columns, int& min_x, int& min_y, int& max_x, int& max_y) {
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
                rows = boost::lexical_cast<int>(split_line.at(2));
                //std::cout << "rows = " << rows << std::endl;
            }
            else if (boost::algorithm::contains(line, "columns")) {
                boost::algorithm::split(split_line, line, boost::algorithm::is_space());
                columns = boost::lexical_cast<int>(split_line.at(2));
                //std::cout << "columns = " << columns << std::endl;
            }
            else if (boost::algorithm::contains(line, "ROI")) {
                boost::algorithm::split(split_line, line, boost::algorithm::is_space());
                min_y = boost::lexical_cast<int>(split_line.at(2));
                min_x = boost::lexical_cast<int>(split_line.at(3));
                max_y = boost::lexical_cast<int>(split_line.at(4));
                max_x = boost::lexical_cast<int>(split_line.at(5));
                //std::cout << "roi = " << min_x << " " << min_y << " " << max_x << " " << max_y << std::endl;
            }
            else if (boost::algorithm::contains(line, "EOH")) {
                header_byte_counter++;
                end_of_header_reached = true;
            }
            line.erase();
        }
    }
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

template<typename T>
    void transpose(T* matrix, int width, int height) {
        int count= width*height;
        for (int x= 0; x<width; ++x) {
            int count_adjustment= width - x - 1;

            for (int y= 0, step= 1; y<height; ++y, step+= count_adjustment)
            {
                int last= count - (y+x*height);
                int first= last - step;

                std::rotate(matrix + first, matrix + first + 1, matrix + last);
            }
        }
    }
}
