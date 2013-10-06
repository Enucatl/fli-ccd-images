#ifndef NEWEST_IMAGE_READER_H
#define NEWEST_IMAGE_READER_H

#include <iostream>
#include <vector>
#include <algorithm>
#include <iterator>
#include <boost/filesystem.hpp>
#include <boost/iterator/filter_iterator.hpp>

#include "base_image_reader.h"

namespace fs = boost::filesystem;

namespace readimages {

class NewestImageReader: public BaseImageReader {

public:
    NewestImageReader(): BaseImageReader() {}

    //never returns!
    //continuously updates histogram if a new file is found
    void update_histogram();

    //never returns!
    //looks for the newest file in path
    //and stores its name in the path_ member, then notifying file_found_
    void set_path(fs::path path);

};

}
#endif /* end of include guard: NEWEST_IMAGE_READER_H */
