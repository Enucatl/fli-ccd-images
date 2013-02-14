#ifndef HORIZONTAL_LINE_H
#define HORIZONTAL_LINE_H

//line that moves vertically on a canvas. Inspired by:
//http://adweb.desy.de/~pcastro/example_progs/index.html#LINE_MOVES

#include "TROOT.h"
#include "TQObject.h"
#include "TLine.h"
#include "TPad.h"

namespace readimages {
namespace gui{

class HorizontalLine : public TLine, public TQObject {
public:
  HorizontalLine(Double_t x1, Double_t y1, Double_t x2, Double_t y2);
  virtual void ExecuteEvent(Int_t event, Int_t px, Int_t py);
};

}
}

#endif /* end of include guard: HORIZONTAL_LINE_H */
