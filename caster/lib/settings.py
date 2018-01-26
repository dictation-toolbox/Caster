import json
import os
import sys
import collections

SETTINGS = {}
_SETTINGS_PATH = os.path.realpath(__file__).split("lib")[0]+"bin\\data\\settings.json"
BASE_PATH = os.path.realpath(__file__).split("\\lib")[0].replace("\\", "/")

# title
SOFTWARE_VERSION_NUMBER = "0.5.9"
SOFTWARE_NAME = "Caster v " + SOFTWARE_VERSION_NUMBER
HOMUNCULUS_VERSION = "HMC v " + SOFTWARE_VERSION_NUMBER
HMC_TITLE_RECORDING = " :: Recording Manager"
HMC_TITLE_DIRECTORY = " :: Directory Selector"
HMC_TITLE_CONFIRM = " :: Confirm"
LEGION_TITLE = "legiongrid"
RAINBOW_TITLE = "rainbowgrid"
DOUGLAS_TITLE = "douglasgrid"
SETTINGS_WINDOW_TITLE = "Caster Settings Window v "

# enums
QTYPE_DEFAULT = "0"
QTYPE_INSTRUCTIONS = "3"
QTYPE_RECORDING = "4"
QTYPE_DIRECTORY = "5"
QTYPE_CONFIRM = "6"
WXTYPE_SETTINGS = "7"

HMC_SEPARATOR = "[hmc]"

WSR = False

def _find_natspeak():
    '''Tries to find the natspeak engine.'''
    possible_locations = [
        "C:/Program Files (x86)/Nuance/NaturallySpeaking15/Program/natspeak.exe",
        "C:/Program Files (x86)/Nuance/NaturallySpeaking14/Program/natspeak.exe",
        "C:/Program Files (x86)/Nuance/NaturallySpeaking13/Program/natspeak.exe",
        "C:/Program Files (x86)/Nuance/NaturallySpeaking12/Program/natspeak.exe",
    ]
    for location in possible_locations:
        if os.path.isfile(location):
            return location
    print "Cannot find default dragon engine path"
    return ""

# The defaults for every setting. Could be moved out into its own file. 
_DEFAULT_SETTINGS = {
    "paths": {
        "BASE_PATH": BASE_PATH,

        # DATA
        "ALIAS_PATH": BASE_PATH + "/bin/data/aliases.json.",
        "CCR_CONFIG_PATH": BASE_PATH + "/bin/data/ccr.json",
        "DLL_PATH": BASE_PATH + "/lib/dll/",
        "FILTER_DEFS_PATH": BASE_PATH + "/user/words.txt",
        "LOG_PATH": BASE_PATH + "/bin/data/log.txt",
        "RECORDED_MACROS_PATH": BASE_PATH + "/bin/data/recorded_macros.json",
        "SAVED_CLIPBOARD_PATH": BASE_PATH + "/bin/data/clipboard.json",
        "SIKULI_SCRIPTS_FOLDER_PATH": BASE_PATH + "/asynch/sikuli/scripts",

        # REMOTE_DEBUGGER_PATH is the folder in which pydevd.py can be found
        "REMOTE_DEBUGGER_PATH": "",

        # EXECUTABLES
        "DEFAULT_BROWSER_PATH": "C:/Program Files (x86)/Mozilla Firefox/firefox.exe",
        "DOUGLAS_PATH": BASE_PATH + "/asynch/mouse/grids.py",
        "ENGINE_PATH": _find_natspeak(),
        "HOMUNCULUS_PATH": BASE_PATH + "/asynch/hmc/h_launch.py",
        "LEGION_PATH": BASE_PATH + "/asynch/mouse/legion.py",
        "MEDIA_PATH": BASE_PATH + "/bin/media",
        "RAINBOW_PATH": BASE_PATH + "/asynch/mouse/grids.py",
        "REBOOT_PATH": BASE_PATH + "/bin/reboot.bat",
        "REBOOT_PATH_WSR": BASE_PATH + "/bin/reboot_wsr.bat",
        "SETTINGS_WINDOW_PATH": BASE_PATH + "/asynch/settingswindow.py",
        "SIKULI_COMPATIBLE_JAVA_EXE_PATH": "",
        "SIKULI_IDE_JAR_PATH": "",
        "SIKULI_SCRIPTS_JAR_PATH": "",
        "SIKULI_SERVER_PATH": BASE_PATH + "/asynch/sikuli/scripts/xmlrpc_server.sikuli",
        "WSR_PATH": "C:/Windows/Speech/Common/sapisvr.exe",

        # CCR
        "CONFIGDEBUGTXT_PATH": BASE_PATH + "/bin/data/configdebug.txt",

        # PYTHON
        "WXPYTHON_PATH": "C:/Python27/Lib/site-packages/wx-3.0-msw"
    },

    # Apps Section
    "apps": {
        "atom": True,
        "chrome": True,
        "cmd": True,
        "dragon": True,
        "eclipse": True,
        "emacs": True,
        "explorer": True,
        "firefox": True,
        "flashdevelop": True,
        "foxitreader": True,
        "gitbash": True,
        "kdiff3": True,
        "douglas": True,
        "legion": True,
        "rainbow": True,
        "ssms": True,
        "jetbrains": True,
        "msvc": True,
        "notepadplusplus": True,
        "sqldeveloper": True,
        "sublime": True,
        "visualstudio": True,
        "winword": True,
        "wsr": True,
    },

    # feature switches
    "feature_rules": {
        "hmc": True,
        "again": True,
        "alias": True,
        "chainalias": True,
    },

    # node rules
    "nodes": {},

    # miscellaneous section
    "miscellaneous": {
        "dev_commands": False,
        "sikuli_enabled": False,
        "keypress_wait": 50, # milliseconds
        "max_ccr_repetitions": 16,
        "atom_palette_wait": "30",
        "rdp_mode": False,
        "integer_remap_opt_in": False,
        "integer_remap_crash_fix": False,
        "print_rdescripts": False,
        "history_playback_delay_secs": 1.0,
    },
    "pronunciations": {
        "c++": "C plus plus",
        "jquery": "J query",
    },
    "one time warnings": {}
}


# Internal Methods
def _save(data, path):
    '''only to be used for settings file'''
    try:
        formatted_data = json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False)
        if not os.path.exists(path):
            f = open(path, "w")
            f.close()
        f = open(path, "w")
        f.write(formatted_data)
        f.close()
    except Exception:
        print "Error saving json file: " + path

def _init(path):
    result = {}
    try:
        f = open(path, "r")
        result = json.loads(f.read())
        f.close()
    except ValueError:
        print("\n\nValueError while loading settings file: " + path + "\n\n")
        print(sys.exc_info())
    except IOError:
        print("\n\nIOError: Could not find settings file: " + path + "\nInitializing file...\n\n")
    result, num_default_added = _deep_merge_defaults(result, _DEFAULT_SETTINGS)
    if num_default_added > 0:
        print "Default settings values added: %d " % num_default_added
        _save(result, _SETTINGS_PATH)
    return result


def _deep_merge_defaults(data, defaults):
    '''
    Recursivly merge data and defaults, preferring data.
    Only handles nested dicts and scalar values.
    Modifies `data` in place.
    '''
    changes = 0
    for key, default_value in defaults.iteritems():
        # If the key is in the data, use that, but call recursivly if it's a dict.
        if(key in data):
            if(isinstance(data[key], collections.Mapping)):
                child_data, child_changes = _deep_merge_defaults(data[key], default_value)
                data[key] = child_data
                changes += child_changes
        else:
            data[key] = default_value
            changes += 1
    return data, changes



# Public interface:
def save_config():
    '''Save the current in-memory settings to disk'''
    _save(SETTINGS, _SETTINGS_PATH)

def get_settings():
    global SETTINGS
    return SETTINGS

def get_default_browser_executable():
    global SETTINGS
    return SETTINGS["paths"]["DEFAULT_BROWSER_PATH"].split("/")[-1]

def report_to_file(message, path=None):
    _path = SETTINGS["paths"]["LOG_PATH"]
    if path is not None: _path = path
    f = open(_path, 'a')
    f.write(str(message) + "\n")
    f.close()


## Kick everything off.
SETTINGS = _init(_SETTINGS_PATH)
for path in [
        SETTINGS["paths"]["REMOTE_DEBUGGER_PATH"],
        SETTINGS["paths"]["WXPYTHON_PATH"]
    ]:
    if not path in sys.path and os.path.isdir(path):
        sys.path.append(path)
