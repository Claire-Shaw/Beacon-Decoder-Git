import sys
from cx_Freeze import setup, Executable
includefiles =["Countries.csv"]
# Dependencies are automatically detected, but it might need fine tuning.

build_exe_options = {"includes" : [ "re", "atexit" ],"packages": ["os"], "excludes": ["tkinter"],'include_files':includefiles,'build_exe':'decode'}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = 'decoder',
        version = "0.1",
        description = "Beacon Hexidecimal Decode",
        options = {"build_exe": build_exe_options},
        executables = [Executable('decoder.py', base=base)])
