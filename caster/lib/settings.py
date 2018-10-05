# -*- coding: utf-8 -*-

import collections
import io
import json
import os
import sys
import errno
import _winreg

SETTINGS = {}
_SETTINGS_PATH = os.path.realpath(__file__).split("lib")[0] + "bin\\data\\settings.json"
BASE_PATH = os.path.realpath(__file__).split("\\lib")[0].replace("\\", "/")

# title
SOFTWARE_VERSION_NUMBER = "0.5.10"
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


# Validates 'Engine Path' in settings.json
def _validate_engine_path():
    if os.path.isfile(_SETTINGS_PATH):
        with io.open(_SETTINGS_PATH, "rt", encoding="utf-8") as json_file:
            data = json.loads(json_file.read())
            engine_path = data["paths"]["ENGINE_PATH"]
            if os.path.isfile(engine_path):
                return engine_path
            else:
                engine_path = _find_natspeak()
                data["paths"]["ENGINE_PATH"] = engine_path
                try:
                    formatted_data = unicode(
                        json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False))
                    with io.open(_SETTINGS_PATH, "w", encoding="utf-8") as json_file:
                        json_file.write(formatted_data)
                        print "Setting engine path to " + engine_path
                except Exception as e:
                    print "Error saving settings file " + str(e) + _SETTINGS_PATH
                return engine_path
    else:
        return _find_natspeak()


# Finds engine 'natspeak.exe' path and verifies supported DNS versions via Windows Registry.
def _find_natspeak():
    print "Searching Windows Registry For DNS..."
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
                    print error
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
                        print " Dragon Naturally Speaking " + str(
                            DnsVersion
                        ) + " is not supported by Caster. Only versions 13 and above are supported. Purchase Dragon Naturally Speaking 13 or above"
    print "Cannot find dragon engine path"
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
        "ENGINE_PATH": _validate_engine_path(),
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
        "firefox": True,
        "flashdevelop": True,
        "foxitreader": True,
        "gitbash": True,
        "gitter": True,
        "kdiff3": True,
        "douglas": True,
        "legion": True,
        "rainbow": True,
        "rstudio": True,
        "ssms": True,
        "jetbrains": True,
        "msvc": True,
        "notepadplusplus": True,
        "sqldeveloper": True,
        "sublime": True,
        "visualstudio": True,
        "visualstudiocode": True,
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
        "keypress_wait": 50,  # milliseconds
        "max_ccr_repetitions": 16,
        "atom_palette_wait": "30",
        "rdp_mode": False,
        "integer_remap_opt_in": False,
        "integer_remap_crash_fix": False,
        "print_rdescripts": False,
        "history_playback_delay_secs": 1.0,
        "legion_vertical_columns": 30,
    },
    "pronunciations": {
        "c++": "C plus plus",
        "jquery": "J query",
    },
    "one time warnings": {},
    "formats": {
        "_default": {
            "text_format": [5, 0],
            "secondary_format": [1, 1],
        },
        "Python": {
            "text_format": [5, 3],
            "secondary_format": [2, 1],
        },
        "CPP": {
            "text_format": [3, 1],
            "secondary_format": [2, 1],
        },
        "Java": {
            "text_format": [3, 1],
            "secondary_format": [2, 1],
        },
        "Javascript": {
            "text_format": [3, 1],
            "secondary_format": [2, 1],
        },
        "HTML": {
            "text_format": [5, 3],
            "secondary_format": [2, 1],
        },
        "CSharp": {
            "text_format": [3, 1],
            "secondary_format": [2, 1],
        },
        "Dart": {
            "text_format": [3, 1],
            "secondary_format": [2, 1],
        },
        "SQL": {
            "text_format": [5, 3],
            "secondary_format": [2, 1],
        },
        "Rust": {
            "text_format": [5, 3],
            "secondary_format": [2, 1],
        },
    }
}


# Internal Methods
def _save(data, path):
    '''only to be used for settings file'''
    try:
        formatted_data = unicode(
            json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False))
        with io.open(path, "wt", encoding="utf-8") as f:
            f.write(formatted_data)
    except Exception:
        print "Error saving json file: " + path


def _init(path):
    result = {}
    try:
        with io.open(path, "rt", encoding="utf-8") as f:
            result = json.loads(f.read())
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


def get_default_browser_executable():
    global SETTINGS
    return SETTINGS["paths"]["DEFAULT_BROWSER_PATH"].split("/")[-1]


def report_to_file(message, path=None):
    _path = SETTINGS["paths"]["LOG_PATH"]
    if path is not None: _path = path
    with io.open(_path, 'at', encoding="utf-8") as f:
        f.write(unicode(message) + "\n")


## Kick everything off.
SETTINGS = _init(_SETTINGS_PATH)
for path in [
        SETTINGS["paths"]["REMOTE_DEBUGGER_PATH"], SETTINGS["paths"]["WXPYTHON_PATH"]
]:
    if not path in sys.path and os.path.isdir(path):
        sys.path.append(path)
