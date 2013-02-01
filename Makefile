SRC_FOLDER=src
INC_FOLDER=include
LIB_FOLDER=lib
CFLAGS=-Wall `root-config --cflags` -I$(INC_FOLDER)/
LDFLAGS=`root-config --glibs`
BOOST_LIBS=-lboost_program_options -lboost_filesystem -lboost_system -lboost_thread

all: make_folders online_viewer read_newest single_image_reader raw_image_reader raw_image_tools

online_viewer: $(SRC_FOLDER)/online_viewer.cpp rootstyle raw_image_tools raw_image_reader read_newest 
	g++ -o online_viewer $(SRC_FOLDER)/online_viewer.cpp $(LIB_FOLDER)/read_newest.o $(LIB_FOLDER)/rootstyle.o $(LIB_FOLDER)/raw_image_reader.o $(LIB_FOLDER)/raw_image_tools.o $(CFLAGS) $(LDFLAGS) $(BOOST_LIBS) $(INC_STYLE)

single_image_reader: rootstyle raw_image_tools raw_image_reader $(SRC_FOLDER)/single_image_reader.cpp 
	g++ -o single_image_reader $(SRC_FOLDER)/single_image_reader.cpp $(LIB_FOLDER)/rootstyle.o $(LIB_FOLDER)/raw_image_reader.o $(LIB_FOLDER)/raw_image_tools.o $(CFLAGS) $(LDFLAGS) $(BOOST_LIBS) 

read_newest: make_folders $(SRC_FOLDER)/read_newest.cpp $(INC_FOLDER)/read_newest.h
	g++ -c -o $(LIB_FOLDER)/read_newest.o $(SRC_FOLDER)/read_newest.cpp $(CFLAGS) $(LDFLAGS) $(BOOST_LIBS) 

raw_image_reader: make_folders $(SRC_FOLDER)/raw_image_reader.cpp $(INC_FOLDER)/raw_image_reader.h 
	g++ -c -o $(LIB_FOLDER)/raw_image_reader.o $(SRC_FOLDER)/raw_image_reader.cpp $(CFLAGS) $(LDFLAGS) $(BOOST_LIBS) 

raw_image_tools: make_folders $(SRC_FOLDER)/raw_image_tools.cpp $(INC_FOLDER)/raw_image_tools.h
	g++ -c -o $(LIB_FOLDER)/raw_image_tools.o $(SRC_FOLDER)/raw_image_tools.cpp $(CFLAGS) $(LDFLAGS) $(BOOST_LIBS)

rootstyle: make_folders $(SRC_FOLDER)/rootstyle.cpp $(INC_FOLDER)/rootstyle.h
	g++ -c -o $(LIB_FOLDER)/rootstyle.o $(SRC_FOLDER)/rootstyle.cpp $(CFLAGS) $(LDFLAGS) 

make_folders:
	mkdir -p lib

clean:
	rm -f lib/*.*o python/*.pyc online_viewer single_image_reader
