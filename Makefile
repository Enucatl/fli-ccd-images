SRC_FOLDER=src
INC_FOLDER=include
LIB_FOLDER=lib
CFLAGS=-Wall `root-config --cflags` -I$(INC_FOLDER)/
LDFLAGS=`root-config --glibs`
BOOST_LIBS=-lboost_program_options -lboost_filesystem -lboost_system -lboost_thread

all: online_viewer read_newest single_image_reader raw_image_reader raw_image_tools

online_viewer: $(SRC_FOLDER)/online_viewer.cpp raw_image_tools raw_image_reader read_newest $(SRC_FOLDER)/single_image_reader.cpp
	g++ -o online_viewer $(SRC_FOLDER)/online_viewer.cpp $(SRC_FOLDER)/read_newest.cpp $(SRC_FOLDER)/rootstyle.cpp $(SRC_FOLDER)/raw_image_reader.cpp $(SRC_FOLDER)/raw_image_tools.cpp $(CFLAGS) $(LDFLAGS) $(BOOST_LIBS) $(INC_STYLE)

single_image_reader: raw_image_tools raw_image_reader $(SRC_FOLDER)/single_image_reader.cpp
	g++ -o single_image_reader $(SRC_FOLDER)/single_image_reader.cpp $(SRC_FOLDER)/rootstyle.cpp $(SRC_FOLDER)/raw_image_reader.cpp $(SRC_FOLDER)/raw_image_tools.cpp $(CFLAGS) $(LDFLAGS) $(BOOST_LIBS) 

read_newest: raw_image_tools raw_image_reader $(SRC_FOLDER)/single_image_reader.cpp
	g++ -fPIC -shared -o $(LIB_FOLDER)/read_newest.so $(SRC_FOLDER)/read_newest.cpp $(SRC_FOLDER)/rootstyle.cpp $(SRC_FOLDER)/raw_image_reader.cpp $(SRC_FOLDER)/raw_image_tools.cpp $(CFLAGS) $(LDFLAGS) $(BOOST_LIBS) 

raw_image_reader: $(SRC_FOLDER)/raw_image_reader.cpp $(INC_FOLDER)/raw_image_reader.h raw_image_tools 
	g++ -fPIC -shared -o $(LIB_FOLDER)/raw_image_reader.so $(SRC_FOLDER)/raw_image_reader.cpp $(SRC_FOLDER)/raw_image_tools.cpp $(SRC_FOLDER)/rootstyle.cpp $(CFLAGS) $(LDFLAGS) $(BOOST_LIBS) 

raw_image_tools: $(SRC_FOLDER)/raw_image_tools.cpp $(INC_FOLDER)/raw_image_tools.h
	g++ -fPIC -shared -o $(LIB_FOLDER)/raw_image_tools.so $(SRC_FOLDER)/raw_image_tools.cpp $(CFLAGS) $(LDFLAGS) $(BOOST_LIBS)

clean:
	rm lib/*.so python/*.pyc online_viewer single_image_reader
