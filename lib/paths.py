'''
Created on May 17, 2014

@author: dave
'''
import sys, os

BASE_PATH = r"C:\NatLink\NatLink\MacroSystem"
#os.path.dirname(os.path.abspath(__file__)) + "\\"
if r"\library.zip" in BASE_PATH:# fixes py2exe bug
    BASE_PATH=BASE_PATH.replace(r"\library.zip","")


SETTINGS_PATH = BASE_PATH + "\\data\\settings.json"
ELEMENT_JSON_PATH = BASE_PATH + "\\data\\element.json"
SAVED_CLIPBOARD_PATH = BASE_PATH + "\\data\\clipboard.json"

#REMOTE_DEBUGGER_PATH is the folder in which pydevd.py can be found
REMOTE_DEBUGGER_PATH ="D:\PROGRAMS\NON_install\eclipse\plugins\org.python.pydev_3.4.1.201403181715\pysrc"

ELEMENT_PATH = r"C:\NatLink\NatLink\MacroSystem\exe\homebrew\element\dist\element.exe"
MEDIA_PATH = r"C:\NatLink\NatLink\MacroSystem\media"
GRID_PATH=r"C:\NatLink\NatLink\MacroSystem\exe\homebrew\CustomGrid\dist\CustomGrid.exe"
NIRCMD_PATH=r"C:\NatLink\NatLink\MacroSystem\exe\nircmd\nircmd.exe"
PSTOOLS_PATH=r"C:\NatLink\NatLink\MacroSystem\exe\PSTools"
PSKILL_PATH=r"C:\NatLink\NatLink\MacroSystem\exe\PSTools\pskill.exe"
MMT_PATH =r"C:\NatLink\NatLink\MacroSystem\exe\MultiMonitorTool\MultiMonitorTool.exe"
PY2EXE_PATH=r"C:\NatLink\NatLink\MacroSystem\exe\py2exe"
HOMEBREW_PATH=r"C:\NatLink\NatLink\MacroSystem\exe\homebrew"
LOG_PATH=r"C:\NatLink\NatLink\MacroSystem\data\log.txt"

JAVA_CONFIG_PATH = r"C:\NatLink\NatLink\MacroSystem\data\ccr\configjava.txt"
PYTHON_CONFIG_PATH = r"C:\NatLink\NatLink\MacroSystem\data\ccr\configpython.txt"
HTML_CONFIG_PATH = r"C:\NatLink\NatLink\MacroSystem\data\ccr\confightml.txt"
PASCAL_CONFIG_PATH = r"C:\NatLink\NatLink\MacroSystem\data\ccr\configpascal.txt"
ALPHABET_CONFIG_PATH = r"C:\NatLink\NatLink\MacroSystem\data\ccr\configalphabet.txt"
NAVIGATION_CONFIG_PATH = r"C:\NatLink\NatLink\MacroSystem\data\ccr\confignavigation.txt"


def get_base():
    global BASE_PATH
    return BASE_PATH

def get_element_path():
    global ELEMENT_PATH
    return ELEMENT_PATH

def get_settings_path():
    global SETTINGS_PATH
    return SETTINGS_PATH

def get_element_json_path():
    global ELEMENT_JSON_PATH
    return ELEMENT_JSON_PATH

def get_saved_clipboard_path():
    global SAVED_CLIPBOARD_PATH
    return SAVED_CLIPBOARD_PATH

def get_nircmd():
    global NIRCMD_PATH
    return NIRCMD_PATH

def get_mmt():
    global MMT_PATH
    return MMT_PATH

def get_all_language_configs():
    global JAVA_CONFIG_PATH
    global PYTHON_CONFIG_PATH
    global HTML_CONFIG_PATH
    return [JAVA_CONFIG_PATH, PYTHON_CONFIG_PATH, HTML_CONFIG_PATH, 
            PASCAL_CONFIG_PATH, ALPHABET_CONFIG_PATH,
            NAVIGATION_CONFIG_PATH]

def get_media_path():
    global MEDIA_PATH
    return MEDIA_PATH

def get_log_path():
    global LOG_PATH
    return LOG_PATH


def get_homebrew_path():
    global HOMEBREW_PATH
    return HOMEBREW_PATH

def get_py2exe_path():
    global PY2EXE_PATH
    return PY2EXE_PATH

def get_grid():
    global GRID_PATH
    return GRID_PATH

def get_pstools_path():
    global PSTOOLS_PATH
    return PSTOOLS_PATH

def get_pskill_path():
    global PSKILL_PATH
    return PSKILL_PATH

if not REMOTE_DEBUGGER_PATH in sys.path:
    sys.path.append(REMOTE_DEBUGGER_PATH)