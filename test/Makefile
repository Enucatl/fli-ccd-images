.PHONY: clean all
.SUFFIXES: .cpp .o

SRC_FOLDER=../src
INC_FOLDER=../include
LIB_FOLDER=../lib

vpath %.cpp $(SRC_FOLDER)
vpath %.h $(INC_FOLDER)

CFLAGS=-Wall `root-config --cflags` -I$(INC_FOLDER)/
LDFLAGS=`root-config --glibs`

test_contrast_adjuster: test_contrast_adjuster.cpp $(addprefix $(LIB_FOLDER)/, rootstyle.o contrast_adjuster.o)
	g++ $(CFLAGS) -o $@ $^ $(LDFLAGS) 

$(LIB_FOLDER)/%.o: %.cpp %.h
	g++ -c $(CFLAGS) -o $@ $< 

clean:
	-rm test_contrast_adjuster
