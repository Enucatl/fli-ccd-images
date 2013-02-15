#ifndef MAIN_FRAME_H
#define MAIN_FRAME_H

//virtual main class for the frames of the single and online viewers

#include <iostream>
#include <vector>

#include <boost/ptr_container/ptr_vector.hpp>
#include <boost/scoped_ptr.hpp>

#include "TGFrame.h"
#include "TGMenu.h"
#include "TGTableLayout.h"
#include "TRootEmbeddedCanvas.h"
#include "TApplication.h"

#include "base_image_reader.h"

namespace readimages {
namespace gui{

enum menu_command_identifiers {
    M_FILE_OPEN
};

class MainFrame : public TGMainFrame {
public:
    MainFrame(const TGWindow* p, unsigned int width, unsigned int height);

    //process messages from all menus
    bool ProcessMessage(long message, long par1, long par2);

    //close and terminate programme
    void CloseWindow();

private:
    TGCompositeFrame table_;
    TGTableLayout table_layout_;
    TGLayoutHints layout_hints_;

    //menu
    TGMenuBar menu_bar_;
    TGLayoutHints menu_bar_layout_;
    TGLayoutHints menu_bar_item_layout_;
    TGLayoutHints menu_bar_help_layout_;
    TGPopupMenu file_menu_;

    boost::ptr_vector<TGTableLayoutHints> table_layout_hints_;
    TRootEmbeddedCanvas embedded_canvas_;
    TRootEmbeddedCanvas projection_canvas_;
    TRootEmbeddedCanvas transform_canvas_;

    //reads the image
    boost::scoped_ptr<BaseImageReader> image_reader_;
};

}
}
#endif /* end of include guard: MAIN_FRAME_H */
