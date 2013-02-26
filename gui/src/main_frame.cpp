#include "main_frame.h"

namespace readimages {
namespace gui{

double horizontal_separation_fraction = 0.618;

MainFrame::MainFrame(const TGWindow* window, unsigned int width, unsigned int height):
    TGMainFrame(window, width, height),
    table_(this, width, height),
    table_layout_(&table_, 2, 2),
    layout_hints_(kLHintsTop | kLHintsLeft |
            kLHintsExpandX | kLHintsExpandY),
    menu_bar_(this, 1, 1, kHorizontalFrame),
    menu_bar_layout_(kLHintsTop | kLHintsLeft | kLHintsExpandX, 0, 0, 1, 1),
    menu_bar_item_layout_(kLHintsTop | kLHintsLeft, 0, 4, 0, 0),
    menu_bar_help_layout_(kLHintsTop | kLHintsRight),
    table_layout_hints_(3),
    embedded_canvas_("image_embedded_canvas",
            &table_,
            static_cast<unsigned int>(width * horizontal_separation_fraction),
            height),
    projection_canvas_("projection_canvas",
            &table_,
            static_cast<unsigned int>(width * (1 - horizontal_separation_fraction)),
            height / 2),
    transform_canvas_("transform_canvas",
            &table_,
            static_cast<unsigned int>(width * (1 - horizontal_separation_fraction)),
            height / 2),
    transform_histogram_(0),
    projection_along_pixel_(530),
    style_(setTDRStyle())
{
    //set title
    SetWindowName("ccdfli_viewer");

    //set menus
    AddFrame(&menu_bar_, &menu_bar_layout_);
    menu_bar_.AddPopup("&File", &file_menu_, &menu_bar_item_layout_);
    file_menu_.Associate(this);
    file_menu_.AddEntry("&Open...", M_FILE_OPEN);
    file_menu_.AddEntry("&Close", M_FILE_CLOSE);
    menu_bar_.AddPopup("&View", &view_menu_, &menu_bar_item_layout_);
    view_menu_.Associate(this);
    view_menu_.AddEntry("&Adjust contrast/brightness...", M_CONTRAST);

    //set table
    table_.SetLayoutManager(&table_layout_);
    AddFrame(&table_, &layout_hints_);

    //set main canvas in table
    table_layout_hints_.push_back(new TGTableLayoutHints(
                0, 1, 0, 2,
                kLHintsExpandX | kLHintsExpandY |
                kLHintsShrinkX | kLHintsShrinkY |
                kLHintsFillX | kLHintsFillY));
    table_.AddFrame(&embedded_canvas_, &table_layout_hints_[0]);

    //set projection and transform_canvas in table
    table_layout_hints_.push_back(new TGTableLayoutHints(
                1, 2, 0, 1,
                kLHintsExpandX | kLHintsExpandY |
                kLHintsShrinkX | kLHintsShrinkY |
                kLHintsFillX | kLHintsFillY));
    table_.AddFrame(&projection_canvas_, &table_layout_hints_[1]);
    table_layout_hints_.push_back(new TGTableLayoutHints(
                1, 2, 1, 2,
                kLHintsExpandX | kLHintsExpandY |
                kLHintsShrinkX | kLHintsShrinkY |
                kLHintsFillX | kLHintsFillY));
    table_.AddFrame(&transform_canvas_, &table_layout_hints_[2]);

    //force style
    gROOT->SetStyle("tdrStyle");
    gROOT->ForceStyle();

    transform_canvas_.GetCanvas()->SetLogy();
    table_.Layout();
    MapSubwindows();
    Layout();
    MapWindow();

    embedded_canvas_.GetCanvas()->Connect("ProcessedEvent(int, int, int, TObject*)",
            "readimages::gui::MainFrame", this, "UpdateProjection(int, int, int, TObject*)");

    //initialize file_info_ needed for the dialog
    const char *filetypes[] = {"RAW images", "*.raw", 0, 0};
    file_info_.fFileTypes = filetypes;
    file_info_.fIniDir = StrDup(".");
}

void MainFrame::CloseWindow() {
    // Got close message for this MainFrame. Calls parent CloseWindow()
    // (which destroys the window) and terminate the application.
    // The close message is generated by the window manager when its close
    // window menu item is selected.

    std::cout << "App closing, bye!" << std::endl;
    //
    // you'd better close files here
    //
    TGMainFrame::CloseWindow();
    gApplication->Terminate(0);
}

bool MainFrame::ProcessMessage(long message, long par1, long par2) {
    switch (GET_MSG(message)) {

        case kC_COMMAND:
            switch (GET_SUBMSG(message)) {

                case kCM_MENUSELECT:
                    break;

                case kCM_MENU:
                    //std::cout << "menu pressed " << par1 << "\n" ;
                    switch (par1) {

                        case M_FILE_OPEN:
                            OpenFile();
                            break;

                        case M_FILE_CLOSE:
                            CloseWindow();
                            break;

                        case M_CONTRAST:
                            SpawnContrastAdjustment();
                            break;

                        default:
                            std::cout << "Menu " << par1 << " not programmed\n" ;
                            break;
                    } //end of switch(par1)
            } //end of switch (GET_SUBMSG(message))
            break;
        default:
            break;
    } //end of switch (GET_MSG(message))
    return true;
}

void MainFrame::OpenFile() {
    //lock mutex to prevent the newest image reader from looking into folders
    //while browsing the Dialog
    if (image_reader_) {
        image_reader_->mutex_.lock();
        if (image_reader_thread_.get_id() != not_a_thread_id_)
            std::cout << "calling interrupt image reader thread" << std::endl;
            image_reader_thread_.interrupt();
    }
    //automatically calls delete when the window is closed, according to http://root.cern.ch/phpBB3/viewtopic.php?p=69013#p69013
    dialog_ = new TGFileDialog(gClient->GetRoot(), this, kFDOpen, &file_info_);
    if (image_reader_)
        image_reader_->mutex_.unlock();
    //start in new thread 
    if (file_info_.fFilename and image_reader_thread_.get_id() != not_a_thread_id_) {
        image_reader_thread_ = boost::thread(&MainFrame::LaunchImageReader, this, file_info_.fFilename);
    }
}

void MainFrame::LaunchImageReader(fs::path path) {
    //never returns! start in new thread!
    if (not fs::exists(path))
        return;
    else if (fs::is_directory(path)) 
        image_reader_.reset(new NewestImageReader());
    else if (fs::is_regular_file(path))
        image_reader_.reset(new SingleImageReader());
    //with this version, it is not possible to stop the threads without
    //closing the app. Therefore, in order to switch the behaviour from
    //"online viewer" to "single viewer" you have to restart it.

    set_path_thread_ = boost::thread(&readimages::BaseImageReader::set_path, image_reader_.get(), path);
    update_hist_thread_ = boost::thread(&readimages::BaseImageReader::update_histogram, image_reader_.get());
    while (true) {
        //wait for calculation of fourier transform in the previous loop
        //cycle
        boost::mutex::scoped_lock lock(image_reader_->mutex_);
        image_reader_->histogram_drawn_.wait(lock);
        DrawImage();
        DrawProjection();
        //start in separate thread because it is time consuming
        DrawTransform();
    }
}

void MainFrame::DrawImage() {
    boost::mutex::scoped_lock lock(drawing_mutex_);
    embedded_canvas_.GetCanvas()->cd();
    image_reader_->Draw("col");
    embedded_canvas_.GetCanvas()->Modified();
    embedded_canvas_.GetCanvas()->Update();
}

void MainFrame::DrawProjection() {
    boost::mutex::scoped_lock lock(drawing_mutex_);
    projection_canvas_.GetCanvas()->cd();
    int pixel = projection_along_pixel_ - embedded_canvas_.GetCanvas()->GetUymin();
    projection_histogram_ = image_reader_->ProjectionX("projection", pixel, pixel);
    std::string new_title = "Along pixel " + boost::lexical_cast<std::string>(projection_along_pixel_);
    projection_histogram_->SetTitle(new_title.c_str());
    projection_histogram_->Draw();
    projection_canvas_.GetCanvas()->Modified();
    projection_canvas_.GetCanvas()->Update();
}

void MainFrame::DrawTransform() {
    boost::mutex::scoped_lock lock(drawing_mutex_);
    transform_canvas_.GetCanvas()->cd();
    transform_histogram_ = projection_histogram_->FFT(transform_histogram_, "MAG R2C");
    transform_histogram_->SetTitle("Fourier transform of above histogram");
    transform_histogram_->Draw();
    transform_canvas_.GetCanvas()->Modified();
    transform_canvas_.GetCanvas()->Update();
}

void MainFrame::SpawnContrastAdjustment() {
    contrast_adjuster_canvas_.reset(new TCanvas("contrast adjustment", "contrast adjustment", 200, 400));
    contrast_adjuster_.reset(new ContrastAdjuster());
    contrast_adjuster_canvas_->SetWindowPosition(1000, 400);
    contrast_adjuster_->set_parent_canvas(embedded_canvas_.GetCanvas());
    contrast_adjuster_->set_my_canvas(contrast_adjuster_canvas_.get());
    contrast_adjuster_->set_style(&style_);
    contrast_adjuster_->get_intensity_distribution(image_reader_->get_histogram());
    contrast_adjuster_->Draw();
}

void MainFrame::UpdateProjection(int event, int x, int y, TObject* selected) {
    if (event == kButton1Double) {
        projection_along_pixel_ = embedded_canvas_.GetCanvas()->AbsPixeltoY(y);
        DrawProjection();
        DrawTransform();
    }
}

}
}
