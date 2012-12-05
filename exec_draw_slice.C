// echo object at mouse position and show a graphics line
void exec_draw_slice() {
    //example of macro called when a mouse event occurs in a pad.
    // Example:
    // Root > TFile f("hsimple.root");
    // Root > hpxpy.Draw();
    // Root > c1.AddExec("exec_draw_slice",".x exec_draw_slice.C");
    // When moving the mouse in the canvas, a second canvas shows the
    // projection along X of the bin corresponding to the Y position
    // of the mouse. The resulting histogram is fitted with a gaussian.
    // A "dynamic" line shows the current bin position in Y.
    // This more elaborated example can be used as a starting point
    // to develop more powerful interactive applications exploiting CINT
    // as a development engine.
    //Author: Rene Brun

    TObject *select = gPad->GetSelected();
    if(!select) return;
    if (!select->InheritsFrom(TH2::Class())) {
        gPad->SetUniqueID(0);
        return;
    }
    gPad->GetCanvas()->FeedbackMode(kTRUE);

    //only run on mouse click
    int event = gPad->GetEvent();
    int px = gPad->GetEventX();
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

    //create or set the new canvas slice_canvas
    TVirtualPad *padsav = gPad;
    TCanvas *slice_canvas = static_cast<TCanvas*>(gROOT->GetListOfCanvases()->FindObject("slice_canvas"));
    if (slice_canvas)
        delete slice_canvas->GetPrimitive("slice");
    else
        slice_canvas = new TCanvas("slice_canvas");

    slice_canvas->cd();
    //draw slice corresponding to mouse position
    TH2 *h = dynamic_cast<TH2*>(select);
    int biny = h->GetYaxis()->FindBin(y);
    TH1D *hp = h->ProjectionX("slice", biny, biny);
    std::stringstream title;
    title << "Slice at y bin " << biny;
    hp->SetTitle(title.str().c_str());
    hp->Draw();
    slice_canvas->Update();
    padsav->cd();
}
