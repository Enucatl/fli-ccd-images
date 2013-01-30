CFLAGS=-Wall `root-config --cflags`
LDFLAGS=`root-config --glibs`
BOOST_LIBS=-lboost_program_options -lboost_system -lboost_filesystem

read_raw_image: read_raw_image.cpp read_raw_image.h
	g++ -c read_raw_image.cpp $(CFLAGS) $(LDFLAGS)

clean:
	rm *.so *.d *.o *_.cxx
