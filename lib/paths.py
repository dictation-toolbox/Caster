'''
Created on May 17, 2014

@author: dave
'''
import sys, os

BASE_PATH = r"C:\NatLink\NatLink\MacroSystem"
#os.path.dirname(os.path.abspath(__file__)) + "\\"
if r"\library.zip" in BASE_PATH:# fixes py2exe bug
    BASE_PATH=BASE_PATH.replace(r"\library.zip","")


SETTINGS_PATH = BASE_PATH + "\\bin\\data\\settings.json"
ELEMENT_JSON_PATH = BASE_PATH + "\\bin\\data\\element.json"
SAVED_CLIPBOARD_PATH = BASE_PATH + "\\bin\\data\\clipboard.json"

#REMOTE_DEBUGGER_PATH is the folder in which pydevd.py can be found
REMOTE_DEBUGGER_PATH ="D:\PROGRAMS\NON_install\eclipse\plugins\org.python.pydev_3.4.1.201403181715\pysrc"

ELEMENT_PATH = r"C:\NatLink\NatLink\MacroSystem\bin\homebrew\element\dist\element.exe"
MEDIA_PATH = r"C:\NatLink\NatLink\MacroSystem\bin\media"
GRID_PATH=r"C:\NatLink\NatLink\MacroSystem\bin\homebrew\CustomGrid\dist\CustomGrid.exe"
NIRCMD_PATH=r"C:\NatLink\NatLink\MacroSystem\bin\nircmd\nircmd.exe"
PSTOOLS_PATH=r"C:\NatLink\NatLink\MacroSystem\bin\PSTools"
PSKILL_PATH=r"C:\NatLink\NatLink\MacroSystem\bin\PSTools\pskill.exe"
MMT_PATH =r"C:\NatLink\NatLink\MacroSystem\bin\MultiMonitorTool\MultiMonitorTool.exe"
PY2EXE_PATH=r"C:\NatLink\NatLink\MacroSystem\bin\py2exe"
HOMEBREW_PATH=r"C:\NatLink\NatLink\MacroSystem\bin\homebrew"
LOG_PATH=r"C:\NatLink\NatLink\MacroSystem\bin\data\log.txt"

GENERIC_CONFIG_PATH=r"C:\NatLink\NatLink\MacroSystem\bin\data\ccr"
UNIFIED_CONFIG_PATH=r"C:\NatLink\NatLink\MacroSystem\bin\data\ccr\unified\config.txt"

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

def get_generic_config_path():
    global GENERIC_CONFIG_PATH
    return GENERIC_CONFIG_PATH

def get_unified_config_path():
    global UNIFIED_CONFIG_PATH
    return UNIFIED_CONFIG_PATH

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