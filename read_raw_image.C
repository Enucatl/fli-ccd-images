#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <inttypes.h>
#include "TH2.h"
#include <iterator>
#include <algorithm>

template<typename T> 
struct Reader {
    std::istream& operator()(std::istream& is, T& pixel){
        return is.read(reinterpret_cast<char*>(&pixel), sizeof(pixel));
    }
};

void read_raw_image(string file_name, int header_bytes, TH2I& image) {
    std::ifstream file(file_name.c_str(), std::ios::binary);
    int columns = image.GetNbinsX();
    int rows = image.GetNbinsY();
    file.seekg(header_bytes);
    if (not file) {
        std::cout << "file not open!" << std::endl;
    }

    std::cout << std::endl;
    std::cout << file_name << std::endl;
    std::cout << std::endl;
    std::vector<uint16_t> vector;
    vector.reserve(rows * columns);
    Reader<uint16_t> reader;
    uint16_t value = 0;
    std::cout << std::endl;
    while(reader(file, value)) {
        vector.push_back(value);
    }
    for (int i = 0; i < columns; i++) {
        for (int j = 0; j < rows; j++) {
            uint16_t content = vector[i * columns + j];
            image.SetBinContent(
                    i + 1, j + 1,
                    content);
        }
    }
    file.close();
}
