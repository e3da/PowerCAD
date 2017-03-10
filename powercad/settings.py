'''
Created on Feb 24, 2014

@author: anizam
changes made by sxm063: os.path.abspath(); added CACHED_CHAR_PATH since it changes between release/non-release modes  - Nov 23, 2015
Updated Jmain changelog - Aug 10, 2016; 
'''
import os
POWERSYNTH_RELEASE = False

if POWERSYNTH_RELEASE:  # For packaged versions
    DEFAULT_TECH_LIB_DIR = os.path.abspath("tech_lib")
    LAST_ENTRIES_PATH = os.path.abspath("export_data/app_data/last_entries.p")
    ELMER_BIN_PATH = "ELmer 8.2-Release/bin"
    GMSH_BIN_PATH = "gmsh-2.7.0-Windows"
    TEMP_DIR = os.path.abspath("export_data/temp")
    CACHED_CHAR_PATH = os.path.abspath("export_data/cached_thermal") # sxm063
else:   # For debugging and running PowerSynth from Eclipse
    DEFAULT_TECH_LIB_DIR = os.path.abspath("../../../tech_lib")
    LAST_ENTRIES_PATH = os.path.abspath("../../../export_data/app_data/last_entries.p")
    #ELMER_BIN_PATH = ""
    #GMSH_BIN_PATH = ""
    ELMER_BIN_PATH = os.path.abspath("C:/Program Files (x86)/Elmer 8.2-Release/bin")     # Default Elmer 8.2 installation directory
    GMSH_BIN_PATH = os.path.abspath("C:/gmsh-2.7.0")     # Default gmsh 2.7.0 installation directory
    TEMP_DIR = os.path.abspath(r"../../../export_data/temp")
    CACHED_CHAR_PATH = os.path.abspath("../../../export_data/cached_thermal") # sxm063

if __name__ == '__main__':  # Module test
    print DEFAULT_TECH_LIB_DIR
    print LAST_ENTRIES_PATH
    print ELMER_BIN_PATH
    print GMSH_BIN_PATH
    print TEMP_DIR
    print CACHED_CHAR_PATH