import sys

BASE_PATH = r"C:\NatLink\NatLink\MacroSystem"
if r"\library.zip" in BASE_PATH:  # fixes py2exe bug
    BASE_PATH = BASE_PATH.replace(r"\library.zip", "")

# DATA
DLL_PATH = r"C:\NatLink\NatLink\MacroSystem\lib\dll\\"
SETTINGS_PATH = BASE_PATH + "\\bin\\data\\settings.json"
ELEMENT_JSON_PATH = BASE_PATH + "\\bin\\data\\element.json"
DISPEL_JSON_PATH = BASE_PATH + "\\bin\\data\\dispel.json"
SAVED_CLIPBOARD_PATH = BASE_PATH + "\\bin\\data\\clipboard.json"
MONITOR_INFO_PATH = BASE_PATH + "\\bin\\data\\monitorscans\\"
LOG_PATH = r"C:\NatLink\NatLink\MacroSystem\bin\data\log.txt"

# REMOTE_DEBUGGER_PATH is the folder in which pydevd.py can be found
REMOTE_DEBUGGER_PATH = "D:\PROGRAMS\NON_install\eclipse\plugins\org.python.pydev_3.4.1.201403181715\pysrc"
if not REMOTE_DEBUGGER_PATH in sys.path:
    sys.path.append(REMOTE_DEBUGGER_PATH)

# EXECUTABLES
WSR_PATH=r"C:\Windows\Speech\Common\sapisvr.exe"
ELEMENT_PATH = r"C:\NatLink\NatLink\MacroSystem\asynch\element_src.py"
LEGION_PATH = r"C:\NatLink\NatLink\MacroSystem\asynch\legion.py"
RAINBOW_PATH = r"C:\NatLink\NatLink\MacroSystem\lib\display.py"
DOUGLAS_PATH = r"C:\NatLink\NatLink\MacroSystem\lib\display.py"
HOMUNCULUS_PATH = r"C:\NatLink\NatLink\MacroSystem\asynch\hmc\homunculus.py"
NIRCMD_PATH = r"C:\NatLink\NatLink\MacroSystem\bin\nircmd\nircmd.exe"
MMT_PATH = r"C:\NatLink\NatLink\MacroSystem\bin\MultiMonitorTool\MultiMonitorTool.exe"


# CCR
GENERIC_CONFIG_PATH = r"C:\NatLink\NatLink\MacroSystem\bin\data\ccr"
UNIFIED_CONFIG_PATH = r"C:\NatLink\NatLink\MacroSystem\bin\data\ccr\unified\config.txt"

# MISC
ALARM_SOUND_PATH = r"C:\NatLink\NatLink\MacroSystem\bin\media\49685__ejfortin__nano-blade-loop.wav"
MEDIA_PATH = r"C:\NatLink\NatLink\MacroSystem\bin\media"
HOMEBREW_PATH = r"C:\NatLink\NatLink\MacroSystem\bin\homebrew"
