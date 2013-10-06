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

    //accessing the axis dimensions, useful for the line drawing the
    //projection
    double get_histogram_x_min() {return histogram_.GetXaxis()->GetXmin();}
    double get_histogram_x_max() {return histogram_.GetXaxis()->GetXmax();}

    //get the projection
    //just a layer on TH2::ProjectionX
    TH1D* ProjectionX(const char* name="_px", int firstybin=0, int lastybin=-1, const char* option="") {return histogram_.ProjectionX(name, firstybin, lastybin, option);}
    //expose TH1::Divide
    bool Divide(const TH1* h) { return histogram_.Divide(h); }

    //Write to a ROOT file
    int Write(const char* name=0, int option=0, int bufsize=0) { return histogram_.Write(name, option, bufsize); }

    raw_image_tools::ImageInfo* get_image_info_ptr() {return &image_info_;}
    raw_image_tools::Image* get_histogram_ptr() {return &histogram_;}

    boost::mutex mutex_; //for the threads
    boost::condition_variable file_found_; //signals that a file has been found
    boost::condition_variable histogram_drawn_; //signals that the histogram is ready to be drawn

protected:
    void read_file(); //loads file (path_) into histogram
    fs::path path_;
    raw_image_tools::Image histogram_;
    raw_image_tools::ImageInfo image_info_;
};

}

#endif /* end of include guard: BASE_IMAGE_READER_H */
