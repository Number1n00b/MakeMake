import configparser
import sys
import os

def main():
    print("MakeMake by Chris.")

    config = configparser.ConfigParser()

    if len(sys.argv) < 2:
        print("No config file provided, using defaults.")
        config["DEFAULT"] = get_defaults()
    else:
        config_filename = sys.argv[1]
        if(os.path.exists(config_filename)):
            print("Reading config file: '{}'.".format(config_filename))
            config.read(config_filename)
        else:
            print("Could not find file: '{}'. Exiting.".format(config_filename))
            return

    config.write(open("test.ini", 'w'))

    print("Done.")



def get_defaults():
    defaults = {}
    defaults["CC"]      = "g++"
    defaults["CFLAGS"]  = "-Wall -pedantic -std=c++11 -g -ggdb"

    defaults["OUT_DIR"] = "bin/obj"
    defaults["EXE_DIR"] = "bin"

    # Check if include directory or lib directories exist and use them if they do.
    defaults["INCLUDE_DIRS"] = get_include_dirs()
    defaults["LIB_DIRS"]     = get_lib_dirs()

    # We should set this later after parsing the #includes of the file.
    defaults["LINK_COMMANDS"] = ""

    defaults["COMPILE_COMMAND"]       = ""
    defaults["COMPILE_WITH_INCLUDES"] = defaults["COMPILE_COMMAND"] + \
                                        " " +  defaults["INCLUDE_DIRS"]

    return defaults


def get_include_dirs():
    return ""

def get_lib_dirs():
    return ""


if __name__ == "__main__":
    main()
