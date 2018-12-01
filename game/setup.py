NAME = "Bi-onic"
VERSION = "0.1"
DESCRIPTION = "As a hybrid of human and machine, when your organic parts start dying, can you use your mechanical components to survive?"
MAIN_FILE = "bi-onic.py"


###########################################
import sys,os
from cx_Freeze import setup,Executable

additional_library = ['numpy.core._methods','numpy.lib.format']
PYTHON_PATH = os.path.dirname(sys.executable)
os.environ['TCL_LIBRARY'] = r'{}\tcl\tcl8.6'.format(PYTHON_PATH)
os.environ['TK_LIBRARY'] = r'{}\tcl\tcl8.6'.format(PYTHON_PATH)

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    executables=[Executable(MAIN_FILE,base = "Win32GUI")],
    options={
            'build_exe': {
                'includes':additional_library,
                'packages':['OpenGL']
                }
            }
    )
