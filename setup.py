# Build an executable for my_script.
# Use command: python setup.py py2exe

import sys
import os

# Yet another *hack* to get py2exe to work.  It can't seem to find win32com.shell.

# ModuleFinder can't handle runtime changes to __path__, but win32com uses them
try:
    # py2exe 0.6.4 introduced a replacement module_finder.
    # This means we have to add package paths there, not to the built-in
    # one.  If this new module_finder gets integrated into Python, then
    # we might be able to revert this some day.
    # if this doesn't work, try import module_finder
    try:
        import py2exe.mf as module_finder
    except ImportError:
        import module_finder
    import win32com
    for p in win32com.__path__[1:]:
        module_finder.AddPackagePath("win32com", p)
    for extra in ["win32com.shell"]:  # ,"win32com.mapi"
        __import__(extra)
        m = sys.modules[extra]
        for p in m.__path__[1:]:
            module_finder.AddPackagePath(extra, p)
except ImportError:
    # no build path setup, no worries.
    pass

from distutils.core import setup
import py2exe

origIsSystemDLL = py2exe.build_exe.isSystemDLL


def is_system_dll(pathname):
        if os.path.basename(pathname).lower() in ("msvcp71.dll", "dwmapi.dll", "mfc71.dll"):
                return 0
        return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = is_system_dll

################################################################

# If run without args, build executable, in quiet mode.
if len(sys.argv) == 1:
    sys.argv.append("py2exe")
    sys.argv.append("-q")


class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        # for the version info resources
        self.version = "1.0.0"
        self.company_name = "MS Company"
        self.copyright = "Copyright 2015 Me. All rights reserved."
        self.name = "FIFA Squad Builder App"


my_script = Target(
    # used for the version info resource
    description="FIFA Squad Builder App",

    # what to build
    script="Main.py",
    dest_base="FIFA Squad Builder")


setup(
    options={"py2exe": {"compressed": 1,
                        "optimize": 2,
                        "ascii": 1,
                        "bundle_files": 3,
                        "packages": ['GUI', 'encodings'],
                        }},
    zipfile=None,
    windows=[my_script]
)
