# ===========================================================================
# Makefile for ASCII Invaders
#
#   make          build it
#   make run      build and run it
#   make clean    delete everything that was built
#
# WARNING: the indented lines below MUST start with a REAL TAB character, not
# spaces. This is a notorious trap, and the error message - "missing separator"
# - does not explain it. Most editors will quietly turn tabs into spaces unless
# you tell them not to.
#
# (The author of this course hit exactly this trap while writing this file.)
# ===========================================================================

CXX      = clang++
CXXFLAGS = -std=c++17 -Wall
TARGET   = invaders
OBJECTS  = main.o game.o screen.o terminal.o

# The DEFAULT rule - the first one in the file. Typing "make" runs this.
# It says: to build invaders you need all the .o files, and the way to make it
# is to LINK them together.
$(TARGET): $(OBJECTS)
	$(CXX) $(OBJECTS) -o $(TARGET)

# A PATTERN rule: how to make ANY .o from the matching .cpp.
#   -c   compile only, do not link
#   $<   the input file      $@   the output file
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Each .o also depends on the headers it includes. Without these lines,
# changing a header would NOT trigger a rebuild - so you would be running
# stale code and wondering why your change did nothing.
main.o:     main.cpp game.h screen.h terminal.h
game.o:     game.cpp game.h screen.h terminal.h
screen.o:   screen.cpp screen.h
terminal.o: terminal.cpp terminal.h

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(OBJECTS) $(TARGET)

# These are not real files, so always run them when asked.
.PHONY: run clean
