CFLAGS=-W -Wall -Wextra -I ../../../include/ -I$(GMOCK_HOME)/include -I$(GMOCK_HOME)/gtest/include -std=c++11

# DEBUG
#CFLAGS+=-g -O0

# PROFILE
#CFLAGS+=-O3 -g -pg  -march=core2 -fstrict-aliasing -DNDEBUG -DEIGEN_NO_MALLOC

# NOT SURE
#CFLAGS+=-O2 -g -DNDEBUG -DEIGEN_NO_MALLOC

# NEED FOR SPEED
CFLAGS+=-O3 -DNDEBUG


LDFLAGS+=-L$(GMOCK_HOME)/osx -L$(GMOCK_HOME)/osx/gtest -lgtest -lgmock
OBJS=cpbconcz2.o modules.o pbsolvercz.o surfconcz.o solvationsub.o subfunction.o
TESTS=solvationsub_test.o surfconcz_test.o

.PHONY: all
all: osm

test: test_main.cpp $(OBJS) $(TESTS)
	$(CXX) $(CFLAGS) -o $@ $^ $(LDFLAGS)

osm: main.cpp $(OBJS)
	$(CXX) $(CFLAGS) -o $@ $^ $(LDFLAGS)

%.o: %.cpp
	$(CXX) $(CFLAGS) -c $<

%.o: ../%.cpp
	$(CXX) $(CFLAGS) -c $<

.PHONY:doc
doc:
	doxygen

.PHONY: clean
clean:
	-rm -rf *.o *.mod osm doc test

