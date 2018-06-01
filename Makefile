# This file was auto-generated by MakeMake.py
CC=g++
CFLAGS=-std=c++11 -Wall -pedantic -g -ggdb -c

EXE_DIR=bin
TEST_DIR=asdasdasd
OBJ_DIR=bin/obj

EXE_NAME=the_program

INCLUDE_DIRS=-I include/SDL2 -I include/glew -I include/glm #-I include/FreeType2

LIB_DIRS=-L lib/glew -L lib/sdl2 #-L lib/FreeType2
LINK_COMMANDS=-lsdl2 -lopengl32 -lglew32 #-lfreetype2

COMPILE_WITH_CFLAGS=$(CC) $(CFLAGS)
COMPILE_WITH_INCLUDES=$(CC) $(CFLAGS) $(INCLUDE_DIRS)

OBJ_FILES=\
	$(OBJ_DIR)/Display.o\
	$(OBJ_DIR)/main.o\
	$(OBJ_DIR)/Drawable.o\
	$(OBJ_DIR)/Entity.o\
	$(OBJ_DIR)/EntityManager.o\
	$(OBJ_DIR)/Shader.o\
	$(OBJ_DIR)/LinkedList.o\
	$(OBJ_DIR)/MathUtil.o\
	$(OBJ_DIR)/Util.o

all: executable

executable: $(OBJ_FILES)
	$(CC) $(OBJ_FILES) -o $(EXE_DIR)/$(EXE_NAME) $(LIB_DIRS) $(LINK_COMMANDS)

$(OBJ_DIR)/Display.o: src/display/Display.cpp \
                      src/display/Display.h \
                      src/main/main.h \
                      src/model/entitymanager.h \
                      src/model/Entity.h \
                      src/util/containers/linkedlist.h
	$(COMPILE_WITH_INCLUDES) src/display/Display.cpp -o $(OBJ_DIR)/Display.o

$(OBJ_DIR)/main.o: src/main/main.cpp \
                   src/main/main.h \
                   src/model/entitymanager.h \
                   src/model/Entity.h \
                   src/util/containers/linkedlist.h \
                   src/display/display.h \
                   src/model/drawable.h \
                   src/model/Shader.h \
                   src/model/shader.h
	$(COMPILE_WITH_INCLUDES) src/main/main.cpp -o $(OBJ_DIR)/main.o

$(OBJ_DIR)/Drawable.o: src/model/Drawable.cpp \
                       src/model/Drawable.h \
                       src/model/Entity.h \
                       src/model/Shader.h
	$(COMPILE_WITH_INCLUDES) src/model/Drawable.cpp -o $(OBJ_DIR)/Drawable.o

$(OBJ_DIR)/Entity.o: src/model/Entity.cpp \
                     src/main/main.h \
                     src/model/entitymanager.h \
                     src/model/Entity.h \
                     src/util/containers/linkedlist.h \
                     src/model/Entity.h
	$(COMPILE_WITH_INCLUDES) src/model/Entity.cpp -o $(OBJ_DIR)/Entity.o

$(OBJ_DIR)/EntityManager.o: \
                            src/model/EntityManager.cpp \
                            src/model/EntityManager.h \
                            src/model/Entity.h \
                            src/util/containers/linkedlist.h \
                            src/model/Drawable.h \
                            src/model/Shader.h
	$(COMPILE_WITH_INCLUDES) src/model/EntityManager.cpp -o $(OBJ_DIR)/EntityManager.o

$(OBJ_DIR)/Shader.o: src/model/Shader.cpp \
                     src/model/Shader.h
	$(COMPILE_WITH_INCLUDES) src/model/Shader.cpp -o $(OBJ_DIR)/Shader.o

$(OBJ_DIR)/LinkedList.o: \
                         src/util/containers/LinkedList.cpp \
                         src/util/containers/LinkedList.h
	$(COMPILE_WITH_INCLUDES) src/util/containers/LinkedList.cpp -o $(OBJ_DIR)/LinkedList.o

$(OBJ_DIR)/MathUtil.o: src/util/MathUtil.cpp \
                       src/util/MathUtil.h
	$(COMPILE_WITH_INCLUDES) src/util/MathUtil.cpp -o $(OBJ_DIR)/MathUtil.o

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

# THIS IS A TEST OF IF IT WORKS LOL
# Clean
.PHONY: clean
clean:
	rm -rf $(OBJ_DIR)/*.o $(EXE_DIR)/$(EXE_NAME) $(EXE_DIR)/*.dll $(TEST_DIR)/* *~*

test:
	echo LOL

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
	@echo "Dam dude... can't even ruin it right. :\\"


