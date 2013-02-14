.PHONY: clean all
.SUFFIXES: .cpp .o

BIN_FOLDER=bin
READIMAGES_FOLDER=readimages
SRC_FOLDER=$(READIMAGES_FOLDER)/src
INC_FOLDER=$(READIMAGES_FOLDER)/include
GUI_SRC_FOLDER=$(GUI_FOLDER)/src
GUI_INC_FOLDER=$(GUI_FOLDER)/include
LIB_FOLDER=lib

vpath %.cpp $(SRC_FOLDER) $(GUI_SRC_FOLDER)
vpath %.h $(INC_FOLDER) $(GUI_INC_FOLDER)

CFLAGS=-Wall `root-config --cflags` -I$(INC_FOLDER)/
LDFLAGS=`root-config --glibs`
BOOST_LIBS=-lboost_program_options -lboost_filesystem -lboost_system
BOOST_THREAD_LIBS=-lboost_thread

all: $(addprefix $(BIN_FOLDER)/, online_viewer single_image_reader)

$(BIN_FOLDER)/online_viewer: online_viewer.cpp\
	$(addprefix $(LIB_FOLDER)/, rootstyle.o raw_image_tools.o raw_image_reader.o read_newest.o contrast_adjuster.o)\
	| $(BIN_FOLDER)
	g++ $(CFLAGS) -o $@ $^ $(LDFLAGS) $(BOOST_LIBS) $(BOOST_THREAD_LIBS)

$(BIN_FOLDER)/single_image_reader: single_image_reader.cpp\
	$(addprefix $(LIB_FOLDER)/, rootstyle.o raw_image_tools.o raw_image_reader.o contrast_adjuster.o)\
	| $(BIN_FOLDER)
	g++ $(CFLAGS) -o $@ $^ $(LDFLAGS) $(BOOST_LIBS) 

$(LIB_FOLDER)/%.o: %.cpp %.h | $(LIB_FOLDER)
	g++ -c $(CFLAGS) -o $@ $< 

$(LIB_FOLDER):
	mkdir -p $(LIB_FOLDER)

$(BIN_FOLDER):
	mkdir -p $(BIN_FOLDER)

clean:
	-rm -rf $(LIB_FOLDER) $(BIN_FOLDER) python/*.pyc
