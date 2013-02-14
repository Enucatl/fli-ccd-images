#ifndef MAIN_FRAME_H
#define MAIN_FRAME_H

#include <iostream>
#include <vector>

#include "TGFrame.h"
#include "TGTableLayout.h"

namespace readimages {
namespace gui{

class MainFrame : public TGMainFrame {
public:
    MainFrame(const TGWindow* p, unsigned int width, unsigned int height);
    CloseWindow();

private:
    TGCompositeFrame table_;
    TGTableLayout table_layout_;
    TGLayoutHints layout_hints_;
    std::vector<TGTableLayoutHints> table_layout_hints_;
    TRootEmbeddedCanvas embedded_canvas_;
    TRootEmbeddedCanvas projection_canvas_;
    TRootEmbeddedCanvas transform_canvas_;
};

}
}
#endif /* end of include guard: MAIN_FRAME_H */
