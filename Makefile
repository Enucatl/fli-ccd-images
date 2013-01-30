CFLAGS=-Wall `root-config --cflags`
LDFLAGS=`root-config --glibs`
BOOST_LIBS=-lboost_program_options -lboost_filesystem -lboost_system
INC_STYLE=-I/home/abis_m/bin

read_newest: raw_image_tools raw_image_reader single_image_reader.cpp
	g++ -o read_newest read_newest.cpp ~/bin/rootstyle.cpp raw_image_reader.o raw_image_tools.o $(CFLAGS) $(LDFLAGS) $(BOOST_LIBS) $(INC_STYLE)

single_image_reader: raw_image_tools raw_image_reader single_image_reader.cpp
	g++ -o single_image_reader single_image_reader.cpp ~/bin/rootstyle.cpp raw_image_reader.o raw_image_tools.o $(CFLAGS) $(LDFLAGS) $(BOOST_LIBS) $(INC_STYLE)

raw_image_reader: raw_image_tools raw_image_reader.cpp raw_image_reader.h
	g++ -c raw_image_reader.cpp raw_image_tools.cpp ~/bin/rootstyle.cpp $(CFLAGS) $(LDFLAGS)     $(BOOST_LIBS) $(INC_STYLE)

raw_image_tools: raw_image_tools.cpp raw_image_tools.h
	g++ -c raw_image_tools.cpp $(CFLAGS) $(LDFLAGS) 

clean:
	rm *.so *.d *.o *_.cxx
