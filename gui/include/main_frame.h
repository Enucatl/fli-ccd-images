#ifndef MAIN_FRAME_H
#define MAIN_FRAME_H

//virtual main class for the frames of the single and online viewers

#include <iostream>
#include <vector>

#ifndef __CINT__
#include <boost/ptr_container/ptr_vector.hpp>
#include <boost/scoped_ptr.hpp>
#include <boost/filesystem.hpp>
#include <boost/thread.hpp>
#else
namespace boost {
template<typename T>
class ptr_vector<T>;

template<typename T>
class scoped_ptr<T>;

class thread;

namespace filesystem {
class path;

}
}
#endif

#include "Rtypes.h" //classdef and classimp
#include "TGFrame.h"
#include "TGMenu.h"
#include "TGTableLayout.h"
#include "TRootEmbeddedCanvas.h"
#include "TApplication.h"
#include "TGFileDialog.h"
#include "TCanvas.h"
#include "TH1.h"
#include "TH2.h"

#ifndef __CINT__
#include "base_image_reader.h"
#include "single_image_reader.h"
#include "newest_image_reader.h"
#include "horizontal_line.h"
#else
class BaseImageReader;
class SingleImageReader;
class NewestImageReader;
class HorizontalLine;
#endif

namespace fs = boost::filesystem;

namespace readimages {
namespace gui{

enum menu_command_identifiers {
    M_FILE_OPEN,
    M_FILE_CLOSE
};

class MainFrame : public TGMainFrame {
public:
    MainFrame(const TGWindow* p, unsigned int width, unsigned int height);

    //process messages from all menus
    bool ProcessMessage(long message, long par1, long par2);

    //choose file or folder to open
    void OpenFile();
    void LaunchImageReader(fs::path path);

    //Draw projection in top right canvas
    void DrawProjection(int pixel=40);

    //Draw fourier transform of projection in bottom right canvas
    void DrawTransform();

    //close and terminate programme
    void CloseWindow();

private:
    //draws the horizontal line selecting the pixel along which to show the
    //projection (slice)
    void DrawHorizontalLine();

    //main table
    TGCompositeFrame table_;
    TGTableLayout table_layout_;
    TGLayoutHints layout_hints_;

    //menu
    TGMenuBar menu_bar_;
    TGLayoutHints menu_bar_layout_;
    TGLayoutHints menu_bar_item_layout_;
    TGLayoutHints menu_bar_help_layout_;
    TGPopupMenu file_menu_;

    //open file or directory
    TGFileInfo file_info_;
    TGFileDialog* dialog_;

    //canvases
    boost::ptr_vector<TGTableLayoutHints> table_layout_hints_;
    TRootEmbeddedCanvas embedded_canvas_;
    TRootEmbeddedCanvas projection_canvas_;
    TRootEmbeddedCanvas transform_canvas_;

    //histograms
    TH1D* projection_histogram_;
    TH1* transform_histogram_;

    //projection line
    boost::scoped_ptr<HorizontalLine> horizontal_line_;


    //reads the image online or single
    boost::scoped_ptr<BaseImageReader> image_reader_;

public:
    ClassDef(MainFrame, 0)  //for ROOT CINT
};

}
}
#endif /* end of include guard: MAIN_FRAME_H */
