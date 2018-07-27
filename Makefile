# This file was auto-generated by MakeMake.py
CC=g++
CFLAGS=-std=c++11 -Wall -pedantic -g -ggdb -c

EXE_DIR=./bin
OBJ_DIR=./bin/obj

EXE_NAME=program

INCLUDE_DIRS= # Empty

LIB_DIRS= # Empty
LINK_COMMANDS= # Empty

COMPILE_WITH_CFLAGS=$(CC) $(CFLAGS)
COMPILE_WITH_INCLUDES=$(CC) $(CFLAGS) $(INCLUDE_DIRS)

OBJ_FILES=\
	$(OBJ_DIR)/LinkedList.o \
	$(OBJ_DIR)/StringUtil.o \
	$(OBJ_DIR)/MathUtil.o   \
	$(OBJ_DIR)/Logger.o     \
	$(OBJ_DIR)/main.o       \
	$(OBJ_DIR)/Date.o       \
	$(OBJ_DIR)/Util.o       

all: executable

executable: $(OBJ_FILES)
	$(CC) $(OBJ_FILES) -o $(EXE_DIR)/$(EXE_NAME) $(LIB_DIRS) $(LINK_COMMANDS)

$(OBJ_DIR)/main.o: src/main/main.cpp \
                   src/main/main.h \
                   src/util/StringUtil.h \
                   src/model/Date.h
	$(COMPILE_WITH_INCLUDES) src/main/main.cpp -o $(OBJ_DIR)/main.o

$(OBJ_DIR)/LinkedList.o: \
                         src/model/containers/LinkedList.cpp \
                         src/model/containers/LinkedList.h
	$(COMPILE_WITH_INCLUDES) src/model/containers/LinkedList.cpp -o $(OBJ_DIR)/LinkedList.o

$(OBJ_DIR)/Date.o: src/model/Date.cpp \
                   src/model/Date.h \
                   src/util/StringUtil.h \
                   src/util/Logger.h \
                   src/util/Util.h
	$(COMPILE_WITH_INCLUDES) src/model/Date.cpp -o $(OBJ_DIR)/Date.o

$(OBJ_DIR)/Logger.o: src/util/Logger.cpp \
                     src/util/Logger.h
	$(COMPILE_WITH_INCLUDES) src/util/Logger.cpp -o $(OBJ_DIR)/Logger.o

$(OBJ_DIR)/MathUtil.o: src/util/MathUtil.cpp \
                       src/util/MathUtil.h
	$(COMPILE_WITH_INCLUDES) src/util/MathUtil.cpp -o $(OBJ_DIR)/MathUtil.o

$(OBJ_DIR)/StringUtil.o: src/util/StringUtil.cpp \
                         src/util/StringUtil.h
	$(COMPILE_WITH_INCLUDES) src/util/StringUtil.cpp -o $(OBJ_DIR)/StringUtil.o

$(OBJ_DIR)/Util.o: src/util/Util.cpp \
                   src/util/Util.h
	$(COMPILE_WITH_INCLUDES) src/util/Util.cpp -o $(OBJ_DIR)/Util.o


# Run stuff
.PHONY: run
run:
	./$(EXE_DIR)/$(EXE_NAME)

.PHONY: runVal
runVal:
	valgrind ./$(EXE_DIR)/$(EXE_NAME)


# Clean
.PHONY: clean
clean:
	rm -rf $(OBJ_DIR)/*.o $(EXE_DIR)/$(EXE_NAME) $(EXE_DIR)/*.dll *~*


# Memes
.PHONY: urn
urn:
	@echo "You don't know how to make an urn."


.PHONY: rum
rum:
	@echo "Why is the rum gone?!"


.PHONY: ruin
ruin:
	@echo "You ruined it! :("


.PHONY: riun
riun:
	@echo "Dam dude... can't even ruin it right. :\"

