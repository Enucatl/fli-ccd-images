#include <iostream>

#include "TROOT.h"
#include "TApplication.h"

#include "main_frame.h"

int main(int argc, char **argv) {
    TApplication app("app", &argc, argv);

    if (gROOT->IsBatch()) {
        std::cout << argv[0] << " cannot run in batch mode!" << std::endl;
        return 1;
    }

    readimages::gui::MainFrame viewer(gClient->GetRoot(), 1024, 768);
    app.Run();
    return 0;
}

