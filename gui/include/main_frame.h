#ifndef MAIN_FRAME_H
#define MAIN_FRAME_H

//virtual main class for the frames of the single and online viewers

#include <iostream>
#include <vector>

#include <boost/ptr_container/ptr_vector.hpp>
#include <boost/scoped_ptr.hpp>
#include <boost/filesystem.hpp>
#include <boost/thread.hpp>

#include "TGFrame.h"
#include "TGMenu.h"
#include "TGTableLayout.h"
#include "TRootEmbeddedCanvas.h"
#include "TApplication.h"
#include "TGFileDialog.h"

#include "base_image_reader.h"
#include "single_image_reader.h"
#include "newest_image_reader.h"

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

    //close and terminate programme
    void CloseWindow();

private:
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

    //reads the image online or single
    boost::scoped_ptr<BaseImageReader> image_reader_;
};

}
}
#endif /* end of include guard: MAIN_FRAME_H */
