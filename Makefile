.PHONY: clean all test
.SUFFIXES: .cpp .o

BIN_FOLDER=bin
READIMAGES_FOLDER=readimages
GUI_FOLDER=gui
ANA_FOLDER=analysis
ANA_SRC_FOLDER=$(ANA_FOLDER)/src
SRC_FOLDER=$(READIMAGES_FOLDER)/src
INC_FOLDER=$(READIMAGES_FOLDER)/include
GUI_SRC_FOLDER=$(GUI_FOLDER)/src
GUI_INC_FOLDER=$(GUI_FOLDER)/include
LIB_FOLDER=lib
DICT_FOLDER=$(LIB_FOLDER)/dict
TEST_FOLDER=test

vpath %.cpp $(SRC_FOLDER) $(GUI_SRC_FOLDER) $(TEST_FOLDER) $(DICT_FOLDER) $(ANA_SRC_FOLDER)
vpath %.h $(INC_FOLDER) $(GUI_INC_FOLDER)

CFLAGS=-Wall `root-config --cflags` -I$(INC_FOLDER)/ -I$(GUI_INC_FOLDER) -I$(DICT_FOLDER) -I.
LDFLAGS=`root-config --glibs`
BOOST_LIBS=-lboost_program_options -lboost_filesystem -lboost_system
BOOST_THREAD_LIBS=-lboost_thread

all: $(addprefix $(BIN_FOLDER)/, ccdfli_viewer make_png_and_root intensity_scan)

$(BIN_FOLDER)/ccdfli_viewer: ccdfli_viewer.cpp\
	$(DICT_FOLDER)/main_frameDict.cpp\
	$(addprefix $(LIB_FOLDER)/, rootstyle.o main_frame.o base_image_reader.o newest_image_reader.o single_image_reader.o raw_image_tools.o horizontal_line.o contrast_adjuster.o)\
	| $(BIN_FOLDER)
	g++ $(CFLAGS) -o $@ $^ $(LDFLAGS) $(BOOST_LIBS) $(BOOST_THREAD_LIBS)

$(BIN_FOLDER)/make_png_and_root: make_png_and_root.cpp\
	$(addprefix $(LIB_FOLDER)/, rootstyle.o single_image_reader.o base_image_reader.o raw_image_tools.o)\
	| $(BIN_FOLDER)
	g++ $(CFLAGS) -o $@ $^ $(LDFLAGS) $(BOOST_LIBS) $(BOOST_THREAD_LIBS)

$(BIN_FOLDER)/intensity_scan: intensity_scan.cpp\
	$(addprefix $(LIB_FOLDER)/, rootstyle.o single_image_reader.o base_image_reader.o raw_image_tools.o)\
	| $(BIN_FOLDER)
	g++ $(CFLAGS) -o $@ $^ $(LDFLAGS) $(BOOST_LIBS) $(BOOST_THREAD_LIBS)

$(LIB_FOLDER)/%.o: %.cpp %.h | $(LIB_FOLDER)
	g++ -c $(CFLAGS) -o $@ $< 

$(DICT_FOLDER)/%Dict.cpp: %.h %LinkDef.h | $(DICT_FOLDER)
	rootcint -f $@ -c -p -I$(DICT_FOLDER) -I$(INC_FOLDER) -I$(GUI_INC_FOLDER) $^
	@echo "'Error in <MainFrame>: MainFrame inherits from TObject but does not have its own ClassDef'\n is a known, stupid error and should be ignored"

$(LIB_FOLDER):
	mkdir -p $(LIB_FOLDER)

$(BIN_FOLDER):
	mkdir -p $(BIN_FOLDER)

$(DICT_FOLDER):
	mkdir -p $(DICT_FOLDER)


clean:
	-rm -rf $(DICT_FOLDER) $(LIB_FOLDER) $(BIN_FOLDER) python/*.pyc
