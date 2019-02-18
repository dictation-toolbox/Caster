# -*- coding: utf-8 -*-

import collections
import io
import os
import sys
import toml
import _winreg


SETTINGS = {}
BASE_PATH = os.path.realpath(__file__).rsplit(os.path.sep + "lib", 1)[0].replace("\\", "/")
_USER_DIR = os.path.expanduser("~").replace("\\", "/") + "/.caster"
_SETTINGS_PATH = _USER_DIR + "/data/settings.toml"

for directory in ["data", "rules", "filters", "sikuli"]:
    d = _USER_DIR+"/"+directory
    if not os.path.exists(d):
        os.makedirs(d)

# title
SOFTWARE_VERSION_NUMBER = "0.6.10"
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

def get_filename():
    return _SETTINGS_PATH

def _validate_engine_path():
    '''
    Validates path 'Engine Path' in settings.toml
    '''
    if os.path.isfile(_SETTINGS_PATH):
        with io.open(_SETTINGS_PATH, "rt", encoding="utf-8") as toml_file:
            data = toml.loads(toml_file.read())
            engine_path = data["paths"]["ENGINE_PATH"]
            if os.path.isfile(engine_path):
                return engine_path
            else:
                engine_path = _find_natspeak()
                data["paths"]["ENGINE_PATH"] = engine_path
                try:
                    formatted_data = unicode(toml.dumps(data))
                    with io.open(_SETTINGS_PATH, "w", encoding="utf-8") as toml_file:
                        toml_file.write(formatted_data)
                    print("Setting engine path to ") + engine_path
                except Exception as e:
                    print("Error saving settings file ") + str(e) + _SETTINGS_PATH
                return engine_path
    else:
        return _find_natspeak()


def _find_natspeak():
    '''
    Finds engine 'natspeak.exe' path and verifies supported DNS versions via Windows Registry.
    '''
    print("Searching Windows Registry For DNS...")
    proc_arch = os.environ['PROCESSOR_ARCHITECTURE'].lower()
    proc_arch64 = os.environ['PROCESSOR_ARCHITEW6432'].lower()

    if proc_arch == 'x86' and not proc_arch64:
        arch_keys = {0}
    elif proc_arch == 'x86' or proc_arch == 'amd64':
        arch_keys = {_winreg.KEY_WOW64_32KEY, _winreg.KEY_WOW64_64KEY}
    else:
        raise Exception("Unhandled arch: %s" % proc_arch)

    for arch_key in arch_keys:
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
                              r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0,
                              _winreg.KEY_READ | arch_key)
        for i in xrange(0, _winreg.QueryInfoKey(key)[0]):
            skey_name = _winreg.EnumKey(key, i)
            skey = _winreg.OpenKey(key, skey_name)
            DisplayName, Publisher, DisplayVersion, InstallLocation = 'null'
            try:
                DisplayName = _winreg.QueryValueEx(skey, 'DisplayName')[0]
                Publisher = _winreg.QueryValueEx(skey, 'Publisher')[0]
                DisplayVersion = _winreg.QueryValueEx(skey, 'DisplayVersion')[0]
                InstallLocation = _winreg.QueryValueEx(skey, 'InstallLocation')[0]
            except OSError as error:
                if error.errno == 2:  # Suppresses '[Error 2] The system cannot find the file specified'
                    pass
                else:
                    print(error)
            finally:
                skey.Close()
                if Publisher == "Nuance Communications Inc." and "Dragon" in DisplayName:
                    DnsVersion = int(str(DisplayVersion)[:2])
                    if DnsVersion >= 13:
                        engine_path = InstallLocation.replace(
                            "\\", "/") + "Program/natspeak.exe"
                        if os.path.isfile(engine_path):
                            print "Search Complete."
                            return engine_path
                    else:
                        print(
                            " Dragon Naturally Speaking " + str(DnsVersion) +
                            " is not supported by Caster. Only versions 13 and above are supported. Purchase Dragon Naturally Speaking 13 or above"
                        )
    print("Cannot find dragon engine path")
    return ""


# The defaults for every setting. Could be moved out into its own file.
_DEFAULT_SETTINGS = {
    "paths": {
        "BASE_PATH": BASE_PATH,
        "USER_DIR": _USER_DIR,

        # DATA
        "BRINGME_PATH": _USER_DIR + "/data/bringme.toml",
        "BRINGME_DEFAULTS_PATH": BASE_PATH + "/bin/share/bringme.toml.defaults",
        "ALIAS_PATH": _USER_DIR + "/data/aliases.toml",
        "CCR_CONFIG_PATH": _USER_DIR + "/data/ccr.toml",
        "DLL_PATH": BASE_PATH + "/lib/dll/",
        "FILTER_DEFS_PATH": _USER_DIR + "/data/words.txt",
        "LOG_PATH": _USER_DIR + "/log.txt",
        "RECORDED_MACROS_PATH": _USER_DIR + "/data/recorded_macros.toml",
        "SAVED_CLIPBOARD_PATH": _USER_DIR + "/data/clipboard.toml",
        "SIKULI_SCRIPTS_PATH": _USER_DIR + "/sikuli",

        # REMOTE_DEBUGGER_PATH is the folder in which pydevd.py can be found
        "REMOTE_DEBUGGER_PATH": "",

        # SIKULIX EXECUTABLES
        "SIKULI_IDE": "",
        "SIKULI_RUNNER": "",

        # EXECUTABLES
        "DOUGLAS_PATH": BASE_PATH + "/asynch/mouse/grids.py",
        "ENGINE_PATH": _validate_engine_path(),
        "HOMUNCULUS_PATH": BASE_PATH + "/asynch/hmc/h_launch.py",
        "LEGION_PATH": BASE_PATH + "/asynch/mouse/legion.py",
        "MEDIA_PATH": BASE_PATH + "/bin/media",
        "RAINBOW_PATH": BASE_PATH + "/asynch/mouse/grids.py",
        "REBOOT_PATH": BASE_PATH + "/bin/reboot.bat",
        "REBOOT_PATH_WSR": BASE_PATH + "/bin/reboot_wsr.bat",
        "SETTINGS_WINDOW_PATH": BASE_PATH + "/asynch/settingswindow.py",
        "SIKULI_SERVER_PATH": BASE_PATH + "/asynch/sikuli/server/xmlrpc_server.sikuli",
        "WSR_PATH": "C:/Windows/Speech/Common/sapisvr.exe",

        # CCR
        "CONFIGDEBUGTXT_PATH": _USER_DIR + "/data/configdebug.txt",

        # PYTHON
        "PYTHONW": "C:/Python27/pythonw",
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
        "filedialogue": True,
        "firefox": True,
        "flashdevelop": True,
        "fman": True,
        "foxitreader": True,
        "gitbash": True,
        "gitter": True,
        "kdiff3": True,
        "douglas": True,
        "legion": True,
        "lyx": True,
        "rainbow": True,
        "rstudio": True,
        "ssms": True,
        "jetbrains": True,
        "msvc": True,
        "totalcmd": True,
        "notepadplusplus": True,
        "sqldeveloper": True,
        "sublime": True,
        "visualstudio": True,
        "visualstudiocode": True,
        "winword": True,
        "wsr": True,
    },
    
    # sikuli settings
    "sikuli": {
        "enabled": False,
        "version": ""
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
        "keypress_wait": 50,  # milliseconds
        "max_ccr_repetitions": 16,
        "atom_palette_wait": 30,  # hundredths of a second
        "rdp_mode": False,
        "integer_remap_opt_in": False,
        "integer_remap_crash_fix": False,
        "print_rdescripts": False,
        "history_playback_delay_secs": 1.0,
        "legion_vertical_columns": 30,
        "use_aenea": False,
    },
    "pronunciations": {
        "c++": "C plus plus",
        "jquery": "J query",
    },
    "one time warnings": {},
    "formats": {
        "_default": {
            "text_format": [5, 0],
            "secondary_format": [1, 0],
        },
        "C plus plus": {
            "text_format": [3, 1],
            "secondary_format": [2, 1],
        },
        "C sharp": {
            "text_format": [3, 1],
            "secondary_format": [2, 1],
        },
        "Dart": {
            "text_format": [3, 1],
            "secondary_format": [2, 1],
        },
        "HTML": {
            "text_format": [5, 0],
            "secondary_format": [5, 2],
        },
        "Java": {
            "text_format": [3, 1],
            "secondary_format": [2, 1],
        },
        "Javascript": {
            "text_format": [3, 1],
            "secondary_format": [2, 1],
        },
        "matlab": {
            "text_format": [3, 1],
            "secondary_format": [1, 3],
        },
        "Python": {
            "text_format": [5, 3],
            "secondary_format": [2, 1],
        },
        "Rust": {
            "text_format": [5, 3],
            "secondary_format": [2, 1],
        },
        "sequel": {
            "text_format": [5, 3],
            "secondary_format": [1, 3],
        },
    }
}


# Internal Methods
def _save(data, path):
    '''only to be used for settings file'''
    try:
        formatted_data = unicode(toml.dumps(data))
        with io.open(path, "wt", encoding="utf-8") as f:
            f.write(formatted_data)
    except Exception as e:
        print "Error saving toml file: " + str(e) + _SETTINGS_PATH


def _init(path):
    result = {}
    try:
        with io.open(path, "rt", encoding="utf-8") as f:
            result = toml.loads(f.read())
    except ValueError as e:
        print("\n\n" + repr(e) + " while loading settings file: " + path + "\n\n")
        print(sys.exc_info())
    except IOError as e:
        print("\n\n" + repr(e) + " while loading settings file: " + path +
              "\nAttempting to recover...\n\n")
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
        if (key in data):
            if (isinstance(data[key], collections.Mapping)):
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


def report_to_file(message, path=None):
    _path = SETTINGS["paths"]["LOG_PATH"]
    if path is not None: _path = path
    with io.open(_path, 'at', encoding="utf-8") as f:
        f.write(unicode(message) + "\n")


# Kick everything off.
SETTINGS = _init(_SETTINGS_PATH)
for path in [
        SETTINGS["paths"]["REMOTE_DEBUGGER_PATH"], SETTINGS["paths"]["WXPYTHON_PATH"]
]:
    if not path in sys.path and os.path.isdir(path):
        sys.path.append(path)
