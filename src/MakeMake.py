import subprocess # To run g++ commands to gather dependancies.
import sys # For command line args.
import os  # For file enumeration.

# ========= Configuration Storage ===========
class Config:
    # Always returns a default configuration.
    def __init__(self):
        # Set up environment variables.
        self.project_root_directory = "."
        self.abs_project_root_directory = abspath(self.project_root_directory)

        self.project_source_directory = self.project_root_directory + "/src"
        self.abs_project_source_directory = abspath(self.project_source_directory)

        self.makefile_path = self.project_root_directory + "/Makefile"
        self.abs_makefile_path = abspath(self.makefile_path)

        self.exe_directory = self.project_root_directory + "/bin"

        self.object_directory = self.project_root_directory + "/bin/obj"

        # Set up makefile variables.
        # @TODO I don't actually ever fill these variables in yet.
        self.makevar_include_directories = " # Empty" # Empty until we look through the files.
        self.makevar_lib_directories = " # Empty" # Empty until we look through the files.
        self.makevar_LINK_COMMANDS = " # Empty" # Empty until we look through the files.

        # There are no make rules until we analyse the files.
        self.file_dependancies = {}

        self.makevar_CC = "g++"
        self.makevar_CFLAGS = "-std=c++11 -Wall -pedantic -g -ggdb -c"
        self.makevar_EXE_NAME = "program"
        self.makevar_COMPILE_WITH_CFLAGS = "$(CC) $(CFLAGS)"

        # @TODO Make this only output with files that require it.
        self.makevar_COMPILE_WITH_INCLUDES = "$(CC) $(CFLAGS) $(INCLUDE_DIRS)"

        self.makevar_OBJ_FILES = " # Empty" # Empty until we look through the files.

        # Set up 'allways' makefile code.
        self.copy_pasta = \
"""
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
	@echo "Dam dude... can't even ruin it right. :\\"
"""

    def set_project_root_directory(self, new_root):
        self.project_root_directory = new_root
        self.abs_project_root_directory = abspath(new_root)

        self.set_project_source_directory(new_root + "/src")

    def set_project_source_directory(self, new_source):
        self.project_root_directory = new_source
        self.abs_project_source_directory = abspath(new_source)

    def set_makefile_path(self, new_path):
        self.makefile_path = new_path
        self.abs_makefile_path = abspath(new_path)

# ========== Self Defined Errors ============
class InvalidFileFormatError(Exception):
    def __init__(self, message):
        super().__init__(message)


# ============= Main Program ================


def main():
    print("Running MakeMake...")

    config = Config()

    if(len(sys.argv) > 1):
        print("Creating makefile from root '{}'".format(sys.argv[1]))
        config.set_project_root_directory(sys.argv[1])

        if(len(sys.argv) > 2 and sys.argv[2].startswith("--")):
            config.set_makefile_path(sys.argv[2].split("=")[-1])
    else:
        print("Creating default makefile...")

    discover_dependancies(config)

    print("\nEnsuring path format correctness...")
    make_dependancy_paths_relative(config)
    fix_dependancy_path_format(config)
    fix_dependancy_path_capitilisation(config)

    print("\nWriting to '{}'...".format(config.abs_makefile_path))
    create_makefile(config)

    print("Done")

    return 0

def make_dependancy_paths_relative(config):
    for rule in config.file_dependancies.keys():
        config.file_dependancies[rule] = remove_proj_root_from_path(config.file_dependancies[rule], config.abs_project_root_directory)


def fix_dependancy_path_format(config):
    for file in config.file_dependancies.keys():
        config.file_dependancies[file] = fix_format(config.file_dependancies[file])


def fix_format(dependancy_list):
    # Make newline characters uniform to linux.
    dependancy_list = dependancy_list.replace("\r", "\n")

    # Prettify the padding.
    padding_length = len(dependancy_list.split(":")[0]) + 2 + len("$(OBJ_DIR)/")
    result = list(dependancy_list)

    prev_char = ''
    for ii in range(0, len(result)):
        if prev_char == '\\':
            result[ii + 1] = padding_length * " "

        prev_char = result[ii]

    result = "".join(result)
    result += "\n"

    return result

def fix_dependancy_path_capitilisation(config):
    keys = list(config.file_dependancies.keys())
    for file in keys:
        uncapitilised_dep_string = config.file_dependancies[file]

        second_half = uncapitilised_dep_string.split(":")[1]
        old_path = second_half.replace(" ", "")
        old_path = old_path.replace("\n", "")
        old_path = old_path.replace("\t", "")
        old_path = old_path.replace("\r", "")

        if old_path[0] == '\\':
            old_path = old_path.replace("\\", "", 1)

        # At this point the old path is a list of dependancies seperated by '\'
        dep_list = old_path.split('\\')
        for dep in dep_list:
            to_be_replaced, replaced_with = find_real_file_name(dep, config)
            config.file_dependancies[file] = config.file_dependancies[file].replace(to_be_replaced, replaced_with)

def find_real_file_name(rel_path, config):
    # Check that the rel path is not just a file in the root directory.
    if("/" in rel_path):
        file = rel_path.split("/")[-1]
        incorrect_relative_split_path = rel_path.split("/")[0:-1]
    else:
        file = rel_path
        incorrect_relative_split_path = [""]

    dir_path = config.abs_project_root_directory # Start at the project root
    for dir in incorrect_relative_split_path:
        dir_path += "/" + dir

    for real_file in os.listdir(dir_path):
        if real_file.lower() == file.lower():
            return rel_path, rel_path.replace(file, real_file)

    raise FileNotFoundError("Could not find real file name for '{}'".format(file))


# ======== Makefile Rule Creation  =========
def discover_dependancies(config):
    print("\nDiscovering makefile rules for source folder '{}'\n".format(config.abs_project_source_directory))

    if not os.path.exists(config.abs_project_source_directory):
        print("Error: The given source directory '{}' does not exist.".format(config.abs_project_source_directory))
        exit(-1)

    total_files = get_all_dependancies(config, config.abs_project_source_directory)

    print("Discovered {} files.".format(total_files))


def get_all_dependancies(config, previous_dir_path, files_checked = 0):
    print("Checking: {}".format(previous_dir_path))

    # Get all files in the current directory.
    for file in os.listdir(previous_dir_path):
        abs_file_path = previous_dir_path + '/' + file

        # Recurse if the file is a directory, else analyze file for dependancies.
        if os.path.isdir(abs_file_path):
            files_checked = get_all_dependancies(config, abs_file_path, files_checked)
        else:
            # Only check c and cpp files.
            if (file.endswith('.c') or file.endswith('.cpp')):
                print("\tFound file: {}".format(file))
                files_checked += 1
                result, _ = run_command(["g++", "-std=c++11", "-MM", abs_file_path])
                result = replace_slashes_with_fwd_slashes(result)

                relative_source_file_path = remove_proj_root_from_path(abs_file_path, config.abs_project_root_directory)

                # At this point the capitalisation is still wrong, and rules
                # don't have relative paths.
                config.file_dependancies[relative_source_file_path] = result

    return files_checked


def replace_slashes_with_fwd_slashes(string):
    result = list(string)
    for ii in range(0, len(result) - 1):
        if result[ii] == '\\' and not result[ii + 1] == '\n' and not result[ii + 2] == '\n':
            result[ii] = "/"

    return "".join(result)

def remove_proj_root_from_path(path, abs_proj_root):
    path = path.replace(abs_proj_root + "/", "")
    path = path.replace(abs_proj_root.lower() + "/", "")
    return path


# ====== Makefile Creation Functions =======
def create_makefile(config):
    # Now that we have all the rules, add a list of OBJ files to the vars.
    obj_file_list = []
    for rule in config.file_dependancies.keys():
        obj_name = config.file_dependancies[rule].split(":")[0]
        obj_file_list.append(obj_name)

    config.makevar_OBJ_FILES = obj_file_list

    with open(config.makefile_path, "w") as makefile:
        makefile.write("# This file was auto-generated by MakeMake.py\n")

        write_makefile_vars(makefile, config)

        write_makefile_rules(makefile, config)

        # Write the rest of the makefile.
        makefile.write(config.copy_pasta + "\n")


def write_makefile_vars(makefile, config):
    makefile.write("CC=" + config.makevar_CC + "\n")
    makefile.write("CFLAGS=" + config.makevar_CFLAGS + "\n" + "\n")

    makefile.write("EXE_DIR=" + config.exe_directory + "\n")
    makefile.write("OBJ_DIR=" + config.object_directory + "\n" + "\n")

    makefile.write("EXE_NAME=" + config.makevar_EXE_NAME + "\n" + "\n")

    makefile.write("INCLUDE_DIRS=" + config.makevar_include_directories + "\n" + "\n")

    makefile.write("LIB_DIRS=" + config.makevar_lib_directories + "\n")
    makefile.write("LINK_COMMANDS=" + config.makevar_LINK_COMMANDS + "\n" + "\n")

    makefile.write("COMPILE_WITH_CFLAGS=" + config.makevar_COMPILE_WITH_CFLAGS + "\n")
    makefile.write("COMPILE_WITH_INCLUDES=" + config.makevar_COMPILE_WITH_INCLUDES + "\n" + "\n")

    obj_files_str = obj_list_to_str(config.makevar_OBJ_FILES)
    makefile.write("OBJ_FILES=" + obj_files_str + "\n" + "\n")

def write_makefile_rules(makefile, config):
    makefile.write("all: executable\n\n")

    makefile.write("executable: $(OBJ_FILES)\n")
    makefile.write("\t$(CC) $(OBJ_FILES) -o $(EXE_DIR)/$(EXE_NAME) $(LIB_DIRS) $(LINK_COMMANDS)\n\n")

    obj_prefix = "$(OBJ_DIR)/"

    for source_name in config.file_dependancies.keys():
        deps = config.file_dependancies[source_name]
        obj_name = deps.split(":")[0]

        makefile.write(obj_prefix + deps)
        command = "\t$(COMPILE_WITH_INCLUDES) " + source_name + " -o " + obj_prefix + obj_name
        makefile.write(command + "\n" + "\n")


def obj_list_to_str(obj_list):
    obj_str = "\\\n"

    obj_prefix = "\t$(OBJ_DIR)/"

    obj_list = sorted(obj_list, key=len, reverse=True)
    if not len(obj_list) == 0:
        max_len = len(obj_list[0])

    for obj in obj_list:
        if obj == obj_list[-1]:
            padding = ""
        else:
            padding = " " * ((max_len - len(obj)) + 1)
        obj_str += obj_prefix + obj + padding + "\\\n"

    # Remove the last trailing '\' and '\n'
    obj_str = obj_str[0:-2]

    return obj_str


# =========== Util ===========
def run_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return str(result.stdout.decode("utf-8"))[0:-1], result

def abspath(path):
    return os.path.abspath(path).replace("\\", "/")

# ======= Entry Point ========
if __name__ == "__main__":
    main()
