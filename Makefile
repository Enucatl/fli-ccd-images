.PHONY: clean all chmod
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

PROFILING=-g
CFLAGS=-Wall `root-config --cflags` -I$(INC_FOLDER)/ -I$(GUI_INC_FOLDER) -I$(DICT_FOLDER) -I. $(PROFILING)
LDFLAGS=`root-config --glibs`
BOOST_LIBS=-lboost_program_options -lboost_filesystem -lboost_system
BOOST_THREAD_LIBS=-lboost_thread
PYTHON_PROGRAMMES=$(addprefix python/,\
				  $(addprefix projections/, export_stack.py projection_stack.py)\
				  $(addprefix alignment/, pitch.py roll.py)\
				  $(addprefix dpc/, dpc_radiography.py phase_drift.py visibility_map.py)\
				  $(addprefix raw_images/, correct.py export_images.py intensity_scan.py)\
					)

all: $(addprefix $(BIN_FOLDER)/, ccdfli_viewer) chmod

$(BIN_FOLDER)/ccdfli_viewer: ccdfli_viewer.cpp\
	$(DICT_FOLDER)/main_frameDict.cpp\
	$(addprefix $(LIB_FOLDER)/, rootstyle.o main_frame.o base_image_reader.o newest_image_reader.o single_image_reader.o raw_image_tools.o contrast_adjuster.o)\
	| $(BIN_FOLDER)
	g++ $(CFLAGS) -o $@ $^ $(LDFLAGS) $(BOOST_LIBS) $(BOOST_THREAD_LIBS)

$(LIB_FOLDER)/%.o: %.cpp %.h raw_image_tools.h | $(LIB_FOLDER)
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

chmod: bash/*.sh
	chmod +x bash/*.sh
	-rm -rf bin/*py?
	cd python; python setup.py develop --user

clean:
	-rm -rf $(DICT_FOLDER) $(LIB_FOLDER) $(BIN_FOLDER)\
		test/png test/gif test/test.root test.root callgrind.out* *debuglog*\
		${HOME}/bin/image_convert_server.py
	find -name "*pyc" -exec rm {} \;
