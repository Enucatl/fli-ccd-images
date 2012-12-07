#include <sstream>
#include <boost/scoped_ptr.hpp>
#include "TVirtualPad.h"
#include "TObject.h"
#include "TCanvas.h"
#include "TH1.h"
#include "TH2.h"



// echo object at mouse position and show a graphics line
void exec_draw_slice(TCanvas& slice_canvas) {
    // When clicking the mouse in the canvas, slice_canvas shows the
    // projection along X of the bin corresponding to the Y position
    // of the mouse.
    // A "dynamic" line shows the current bin position in Y.

    TObject *select = gPad->GetSelected();
    if(!select) return;
    if (!select->InheritsFrom(TH2::Class())) {
        gPad->SetUniqueID(0);
        return;
    }
    gPad->GetCanvas()->FeedbackMode(kTRUE);

    //only run on mouse click
    int event = gPad->GetEvent();
    int py = gPad->GetEventY();
    int pyold = gPad->GetUniqueID();
    float uxmin = gPad->GetUxmin();
    float uxmax = gPad->GetUxmax();
    int pxmin = gPad->XtoAbsPixel(uxmin);
    int pxmax = gPad->XtoAbsPixel(uxmax);
    if(pyold) gVirtualX->DrawLine(pxmin,pyold,pxmax,pyold);
    if (event != 11) return;
    //erase old position and draw a line at current position
    gVirtualX->DrawLine(pxmin,py,pxmax,py);
    gPad->SetUniqueID(py);
    float upy = gPad->AbsPixeltoY(py);
    float y = gPad->PadtoY(upy);

    TVirtualPad *padsav = gPad;
    slice_canvas.cd();
    //draw slice corresponding to mouse position
    TH2 *h = dynamic_cast<TH2*>(select);
    int biny = h->GetYaxis()->FindBin(y);
    TH1D *hp = h->ProjectionX("slice", biny, biny);
    std::stringstream title;
    title << "Slice at y bin " << biny;
    hp->SetTitle(title.str().c_str());
    hp->Draw();
    slice_canvas.Update();
    padsav->cd();
}
