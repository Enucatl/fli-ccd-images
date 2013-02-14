#ifndef MAIN_FRAME_H
#define MAIN_FRAME_H

//virtual main class for the frames of the single and online viewers

#include <iostream>
#include <vector>

#include <boost/ptr_container/ptr_vector.hpp>

#include "TGFrame.h"
#include "TGTableLayout.h"
#include "TRootEmbeddedCanvas.h"
#include "TApplication.h"

#include "raw_image_reader.h"

namespace readimages {
namespace gui{

class MainFrame : public TGMainFrame {
public:
    MainFrame(const TGWindow* p, unsigned int width, unsigned int height);
    void CloseWindow();

private:
    TGCompositeFrame table_;
    TGTableLayout table_layout_;
    TGLayoutHints layout_hints_;
    boost::ptr_vector<TGTableLayoutHints> table_layout_hints_;
    TRootEmbeddedCanvas embedded_canvas_;
    TRootEmbeddedCanvas projection_canvas_;
    TRootEmbeddedCanvas transform_canvas_;
};

}
}
#endif /* end of include guard: MAIN_FRAME_H */
