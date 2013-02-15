#ifndef RAW_IMAGE_READER_H
#define RAW_IMAGE_READER_H

//base class (pure virtual) with common structure for the viewer of a single
//image and the folder watcher

#include "base_image_reader.h"

namespace fs = boost::filesystem;

namespace readimages {

class SingleImageReader: public BaseImageReader {

public:
    SingleImageReader(): BaseImageReader() {}

    //opens image in file path
    void set_path(fs::path path); 

    //updates histogram with information in path_
    void update_histogram(); 
};

}

#endif /* end of include guard: RAW_IMAGE_READER_H */
