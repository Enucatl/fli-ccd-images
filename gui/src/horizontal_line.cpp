#include "horizontal_line.h"

namespace readimages {
namespace gui{

HorizontalLine::HorizontalLine(double x1, double y1, double x2, double y2) : TLine(x1,y1,x2,y2)
{
}

//______________________________________________________________________________
void HorizontalLine::ExecuteEvent(int event, int px, int py) {
    std::cout << "Entering execute event!" << std::endl;
//*-*-*-*-*-*-*-*-*-*-*Execute action corresponding to one event*-*-*-*
//*-*                  =========================================
//  This member function is called when a line is clicked with the locator
//
//  If Left button clicked on one of the line end points, this point
//     follows the cursor until button is released.
//
//  if Middle button clicked, the line is moved parallel to itself
//     until the button is released.
//

   int px1, px2, py1, py2;
   int pxold, pyold, px1old, py1old, px2old, py2old;
   bool P1, P2, L;
   double dpx, dpy, xp1, yp1;
   int dx, dy;

   if (not gPad->IsEditable()) return;
   switch (event) {

   case kButton1Down:
      gVirtualX->SetLineColor(-1);
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
      // P.Castro: points don't move
      P1 = P2 = kFALSE;

      // P.Castro: only line is moved paralell to itself
      L = kTRUE;
      pxold = px; pyold = py;
      gPad->SetCursor(kMove);

      break;

   case kButton1Motion:

      if (P1) {
         gVirtualX->DrawLine(px1old, py1old, px2, py2);
         gVirtualX->DrawLine(px, py, px2, py2);
         px1old = px;
         py1old = py;
      }
      if (P2) {
         gVirtualX->DrawLine(px1, py1, px2old, py2old);
         gVirtualX->DrawLine(px1, py1, px, py);
         px2old = px;
         py2old = py;
      }
      if (L) {
         gVirtualX->DrawLine(px1, py1, px2, py2);
         dx = px-pxold;  dy = py-pyold;
         // P.Castro: move only vertically
         /*px1 += dx;*/ py1 += dy; /*px2 += dx;*/ py2 += dy;
         gVirtualX->DrawLine(px1, py1, px2, py2);
         pxold = px;
         pyold = py;
      }
      break;

   case kButton1Up:

      if (TestBit(kLineNDC)) {
         dpx  = gPad->GetX2() - gPad->GetX1();
         dpy  = gPad->GetY2() - gPad->GetY1();
         xp1  = gPad->GetX1();
         yp1  = gPad->GetY1();
         if (P1) {
            fX1 = (gPad->AbsPixeltoX(px)-xp1)/dpx;
            fY1 = (gPad->AbsPixeltoY(py)-yp1)/dpy;
         }
         if (P2) {
            fX2 = (gPad->AbsPixeltoX(px)-xp1)/dpx;
            fY2 = (gPad->AbsPixeltoY(py)-yp1)/dpy;
         }
         if (L) {
            fX1 = (gPad->AbsPixeltoX(px1)-xp1)/dpx;
            fY1 = (gPad->AbsPixeltoY(py1)-yp1)/dpy;
            fX2 = (gPad->AbsPixeltoX(px2)-xp1)/dpx;
            fY2 = (gPad->AbsPixeltoY(py2)-yp1)/dpy;
         }
      } else {
         if (P1) {
            fX1 = gPad->AbsPixeltoX(px);
            fY1 = gPad->AbsPixeltoY(py);
         }
         if (P2) {
            fX2 = gPad->AbsPixeltoX(px);
            fY2 = gPad->AbsPixeltoY(py);
         }
         if (L) {
            fX1 = gPad->AbsPixeltoX(px1);
            fY1 = gPad->AbsPixeltoY(py1);
            fX2 = gPad->AbsPixeltoX(px2);
            fY2 = gPad->AbsPixeltoY(py2);
         }
      }
      gPad->Modified(kTRUE);
      gVirtualX->SetLineColor(-1);
      std::cout << "New y = " << fY1 << "\n";
      
      break;

   case kButton1Locate:

      ExecuteEvent(kButton1Down, px, py);
      while (1) {
         px = py = 0;
         event = gVirtualX->RequestLocator(1,1,px,py);

         ExecuteEvent(kButton1Motion, px, py);

         if (event != -1) {                     // button is released
            ExecuteEvent(kButton1Up, px, py);
            return;
         }
      }
   }
}

}}
