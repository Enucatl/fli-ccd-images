#ifndef BASE_IMAGE_READER_H
#define BASE_IMAGE_READER_H

//base class (pure virtual) with common structure for the viewer of a single
//image and the folder watcher

#include <iostream>

#include <boost/filesystem.hpp>
#include <boost/thread/mutex.hpp>
#include <boost/thread/condition_variable.hpp>

#include "TH2.h"

#include "raw_image_tools.h"

namespace fs = boost::filesystem;

namespace readimages {

class BaseImageReader {

public:
    BaseImageReader(): histogram_("image_hist", "image_hist",
            1, 0, 1, 1, 0, 1) {}
    virtual ~BaseImageReader() {}
    virtual void Draw(const char* options="") {histogram_.Draw(options);}
    //void because it's impossible to get the return value from a thread
    //anyway (see promises/futures)
    virtual void set_path(fs::path path) = 0; //to be threaded
    virtual void update_histogram() = 0; //to be threaded

protected:
    void read_file(); //loads file (path_) into histogram

    boost::mutex mutex_; //for the threads
    boost::condition_variable file_found_; //signals that a file has been found
    fs::path path_;
    TH2D histogram_;
};

}

#endif /* end of include guard: BASE_IMAGE_READER_H */
