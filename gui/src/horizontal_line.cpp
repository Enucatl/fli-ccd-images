#include "horizontal_line.h"

namespace readimages {
namespace gui{

HorizontalLine::HorizontalLine(double x1, double y1, double x2, double y2) : TLine(x1,y1,x2,y2)
{
    SetLineColor(kWhite);
    SetLineWidth(2);
}

//______________________________________________________________________________
void HorizontalLine::ExecuteEvent(int event, int px, int py) {
    std::cout << "Entering execute event!" << std::endl;
    //*-*-*-*-*-*-*-*-*-*-*Execute action corresponding to one event*-*-*-*
    //*-*                  =========================================
    //  This member function is called when a line is clicked with the locator
    //
    //  the line moves only vertically
    //
    int px1 = 0;
    int px2 = 0;
    int py1 = 0;
    int py2 = 0;
    int pyold = 0;
    double dpx = 0;
    double dpy = 0;
    double xp1 = 0;
    double yp1 = 0;
    int dy = 0;

    if (not gPad->IsEditable()) return;
    switch (event) {

        case kButton1Down:
            TAttLine::Modify();  //Change line attributes only if necessary

            // No break !!!

        case kMouseMotion:

            if (TestBit(kLineNDC)) {
                px1 = gPad->UtoPixel(fX1);
                py1 = gPad->VtoPixel(fY1);
                px2 = gPad->UtoPixel(fX2);
                py2 = gPad->VtoPixel(fY2);
            } else {
                px1 = gPad->XtoAbsPixel(fX1);
                py1 = gPad->YtoAbsPixel(fY1);
                px2 = gPad->XtoAbsPixel(fX2);
                py2 = gPad->YtoAbsPixel(fY2);
            }

            pyold = py;
            gPad->SetCursor(kMove);

            break;

        case kButton1Motion:

            gVirtualX->DrawLine(px1, py1, px2, py2);
            dy = py-pyold;
            //move only vertically
            py1 += dy;
            py2 += dy;
            gVirtualX->DrawLine(px1, py1, px2, py2);
            pyold = py;
            break;

        case kButton1Up:

            if (TestBit(kLineNDC)) {
                dpx  = gPad->GetX2() - gPad->GetX1();
                dpy  = gPad->GetY2() - gPad->GetY1();
                xp1  = gPad->GetX1();
                yp1  = gPad->GetY1();
                fX1 = (gPad->AbsPixeltoX(px1)-xp1)/dpx;
                fY1 = (gPad->AbsPixeltoY(py1)-yp1)/dpy;
                fX2 = (gPad->AbsPixeltoX(px2)-xp1)/dpx;
                fY2 = (gPad->AbsPixeltoY(py2)-yp1)/dpy;
            } else {
                fX1 = gPad->AbsPixeltoX(px1);
                fY1 = gPad->AbsPixeltoY(py1);
                fX2 = gPad->AbsPixeltoX(px2);
                fY2 = gPad->AbsPixeltoY(py2);
            }
            gPad->Modified();
            SetLineColor(kRed);
            std::cout << "New y = " << fY1 << "\n";

            break;

        case kButton1Locate:

            ExecuteEvent(kButton1Down, px, py);
            while (1) {
                px = py = 0;
                event = gVirtualX->RequestLocator(1, 1, px, py);

                ExecuteEvent(kButton1Motion, px, py);

                if (event != -1) {                     // button is released
                    ExecuteEvent(kButton1Up, px, py);
                    return;
                }
            }
    }
}

}}
