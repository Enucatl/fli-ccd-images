#include "main_frame.h"

namespace readimages {
namespace gui{

double golden = 0.618;

MainFrame::MainFrame(const TGWindow* window, unsigned int width, unsigned int height):
    TGMainFrame(window, width, height),
    table_(this, width, height),
    table_layout_(&table_, 2, 2),
    layout_hints_(kLHintsTop | kLHintsLeft |
            kLHintsExpandX | kLHintsExpandY),
    embedded_canvas_("image_embedded_canvas",
        &table_,
        static_cast<unsigned int>(width * golden),
        height),
    projection_canvas_("projection_canvas",
        &table_,
        static_cast<unsigned int>(width * (1 - golden)),
        height / 2),
    transform_canvas_("transform_canvas",
        &table_,
        static_cast<unsigned int>(width * (1 - golden)),
        height / 2),
    {
    AddFrame(&table_, layout_hints_);

    //set main canvas in table
    table_layout_hints_.push_back(TGTableLayoutHints(
        0, 1, 0, 2,
        kLHintsExpandX|kLHintsExpandY |
        kLHintsShrinkX|kLHintsShrinkY |
        kLHintsFillX|kLHintsFillY));
    table_.AddFrame(embedded_canvas_, &table_layout_hints_[0]);

    //set projection and transform_canvas in table
    table_layout_hints_.push_back(TGTableLayoutHints(
        1, 2, 0, 1,
        kLHintsExpandX|kLHintsExpandY |
        kLHintsShrinkX|kLHintsShrinkY |
        kLHintsFillX|kLHintsFillY));
    table_.AddFrame(projection_canvas_, &table_layout_hints_[1]);
    table_layout_hints_.push_back(TGTableLayoutHints(
        1, 2, 1, 2,
        kLHintsExpandX|kLHintsExpandY |
        kLHintsShrinkX|kLHintsShrinkY |
        kLHintsFillX|kLHintsFillY));
    table_.AddFrame(transform_canvas_, &table_layout_hints_[2]);

    table_.Layout();
    MapSubWindows();
    Layout();
    MapWindow();
}

}
}
