#ifndef CONTRAST_ADJUSTER_H
#define CONTRAST_ADJUSTER_H

#include <iostream>

//noncopyable header:
#include <boost/utility.hpp>

#include "TObject.h"
#include "TColor.h"
#include "TCanvas.h"
#include "TPad.h"
#include "TH1.h"
#include "TH2.h"
#include "TSlider.h"
#include "TStyle.h"


namespace root_style {

//helper function to be bound to TCanvas::ProcessEvent

class ContrastAdjuster: public TObject, private boost::noncopyable {
    //inheritance from TObject is necessary in order to get the slider to
    //work using the ExecuteEvent method
    //make non copyable, as the inherited copy and assignment operators
    //would do the wrong thing here if I don't redefine them.
    //There's no need to copy such an object anyway, nor to have STL or ROOT
    //containers have multiple items at the moment
public:
    ContrastAdjuster();
    //still needs to be initialized with set style and set parent canvas
    //in order to work correctly
    void get_intensity_distribution(const TH2& parent_histogram);
    void set_style(TStyle* style) { style_ = style; }
    void set_parent_canvas(TCanvas* parent_canvas) { parent_canvas_ = parent_canvas; }
    void Draw(const char* options="");
    void update_style();
    //overloading TObject::ExecuteEvent
    //only calls update_style (which has a more meaningful name)
    void ExecuteEvent(int event, int px, int py); 

private:
    const int n_bins_; //number of bins for histogram_ 
    TCanvas canvas_;
    TPad histogram_pad_;
    TH1D histogram_;
    TSlider slider_;
    TStyle* style_;
    TCanvas* parent_canvas_;
};

}
#endif /* end of include guard: CONTRAST_ADJUSTER_H */
