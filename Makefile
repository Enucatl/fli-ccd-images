CFLAGS=-Wall `root-config --cflags`
LDFLAGS=`root-config --glibs`
BOOST_LIBS=-lboost_program_options -lboost_filesystem -lboost_system -lboost_thread
INC_STYLE=-I/home/abis_m/bin

online_viewer: online_viewer.cpp raw_image_tools raw_image_reader read_newest single_image_reader.cpp
	g++ -o online_viewer online_viewer.cpp read_newest.cpp rootstyle.cpp raw_image_reader.cpp raw_image_tools.cpp $(CFLAGS) $(LDFLAGS) $(BOOST_LIBS) $(INC_STYLE)

read_newest: raw_image_tools raw_image_reader single_image_reader.cpp
	g++ -c read_newest.cpp ~/bin/rootstyle.cpp raw_image_reader.cpp raw_image_tools.cpp $(CFLAGS) $(LDFLAGS) $(BOOST_LIBS) $(INC_STYLE)

single_image_reader: raw_image_tools raw_image_reader single_image_reader.cpp
	g++ -o single_image_reader single_image_reader.cpp rootstyle.cpp raw_image_reader.cpp raw_image_tools.cpp $(CFLAGS) $(LDFLAGS) $(BOOST_LIBS) $(INC_STYLE)

raw_image_reader: raw_image_reader.cpp raw_image_reader.h raw_image_tools 
	g++ -c raw_image_reader.cpp raw_image_tools.cpp rootstyle.cpp $(CFLAGS) $(LDFLAGS)     $(BOOST_LIBS) $(INC_STYLE)

raw_image_tools: raw_image_tools.cpp raw_image_tools.h
	g++ -c raw_image_tools.cpp $(CFLAGS) $(LDFLAGS) $(BOOST_LIBS)

clean:
	rm *.so *.d *.o *_.cxx
