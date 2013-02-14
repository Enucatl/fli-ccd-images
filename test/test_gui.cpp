#include <iostream>

#include "main_frame.h"

int main(int argc, char **argv) {
    TApplication app("app", &argc, argv);

    if (gROOT->IsBatch()) {
        std::cout << argv[0] << " cannot run in batch mode!" << std::endl;
        return 1;
    }

    readimages::gui::MainFrame viewer(gClient->GetRoot());
    app.Run();
    return 0;
}

