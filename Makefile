.PHONY: clean all
.SUFFIXES: .cpp .o

SRC_FOLDER=src
INC_FOLDER=include
LIB_FOLDER=lib

vpath %.cpp $(SRC_FOLDER)
vpath %.h $(INC_FOLDER)

CFLAGS=-Wall `root-config --cflags` -I$(INC_FOLDER)/
LDFLAGS=`root-config --glibs`
BOOST_LIBS=-lboost_program_options -lboost_filesystem -lboost_system
BOOST_THREAD_LIBS=-lboost_thread

all: online_viewer single_image_reader 

online_viewer: online_viewer.cpp $(addprefix $(LIB_FOLDER)/, rootstyle.o raw_image_tools.o raw_image_reader.o read_newest.o contrast_adjuster.o)
	g++ $(CFLAGS) -o $@ $^ $(LDFLAGS) $(BOOST_LIBS) $(BOOST_THREAD_LIBS)

single_image_reader: single_image_reader.cpp $(addprefix $(LIB_FOLDER)/, rootstyle.o raw_image_tools.o raw_image_reader.o contrast_adjuster.o)
	g++ $(CFLAGS) -o $@ $^ $(LDFLAGS) $(BOOST_LIBS) 

$(LIB_FOLDER)/%.o: %.cpp %.h $(LIB_FOLDER)
	g++ -c $(CFLAGS) -o $@ $< 

$(LIB_FOLDER):
	mkdir -p $(LIB_FOLDER)

clean:
	-rm -r lib python/*.pyc online_viewer single_image_reader
