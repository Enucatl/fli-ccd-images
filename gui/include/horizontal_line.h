#ifndef HORIZONTAL_LINE_H
#define HORIZONTAL_LINE_H

//line that moves vertically on a canvas. Inspired by:
//http://adweb.desy.de/~pcastro/example_progs/index.html#LINE_MOVES

#include <iostream>

#include "TROOT.h"
#include "TQObject.h"
#include "TLine.h"
#include "TPad.h"

namespace readimages {
namespace gui{

class HorizontalLine : public TLine, public TQObject {
public:
  HorizontalLine(double x1, double y1, double x2, double y2);
  virtual void ExecuteEvent(int event, int px, int py);
};

}
}

#endif /* end of include guard: HORIZONTAL_LINE_H */
