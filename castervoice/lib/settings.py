# -*- coding: utf-8 -*-

from __future__ import print_function

import collections
import io
import os
import sys
import tomlkit
import _winreg
import version
import errno

GENERIC_HELP_MESSAGE = """
If you continue having problems with this or any other issue you can contact
us through Gitter at <https://gitter.im/dictation-toolbox/Caster> or on our GitHub
issue tracker at <https://github.com/dictation-toolbox/Caster/issues>.
Thank you for using Caster!
"""

SETTINGS = {}
BASE_PATH = os.path.realpath(__file__).rsplit(os.path.sep + "lib",
                                              1)[0].replace("\\", "/")


def set_user_dir():
    '''
    Sets Caster's user directory path. Returns "user_dir" with valid path for Home directory or AppData.
    '''
    user_dir = 'empty_path'
    try:
        directory = os.path.expanduser("~")
        if os.access(directory, os.W_OK) and os.access(directory, os.R_OK) is True:
            user_dir = directory
        else:
            if os.name == 'nt':
                directory = os.path.expandvars(r'%APPDATA%')
                if os.access(directory,
                             os.W_OK) and os.access(directory, os.R_OK) is True:
                    user_dir = directory
    except IOError as e:
        if e.errno == errno.EACCES:
            print("Caster does not have read/write for a user directory. \n" +
                  errno.EACCES)
    finally:
        if os.path.exists(user_dir):
            return os.path.normpath(os.path.join(user_dir, ".caster"))
        else:
            print("Caster could not find a valid user directory at: " + str(user_dir))
            raise NameError('UserPathException')


def validate_user_dir():
    '''
    Checks for existing Caster's user directory path. Returns path.
    '''
    user_dir = os.path.join(os.path.expanduser("~"), ".caster")
    if os.path.exists(user_dir) is True:
        return user_dir
    if os.name == 'nt':
        app_data = os.path.join(os.path.expandvars(r'%APPDATA%'), ".caster")
        if os.path.exists(app_data) is True:
            return app_data
        else:
            return set_user_dir()
    else:
        return set_user_dir()


_USER_DIR = validate_user_dir()
_SETTINGS_PATH = os.path.normpath(os.path.join(_USER_DIR, "data/settings.toml"))

print("Caster User Directory: " + _USER_DIR)

for directory in ["data", "rules", "filters", "sikuli"]:
    d = _USER_DIR + "/" + directory
    if not os.path.exists(d):
        os.makedirs(d)

# title
SOFTWARE_VERSION_NUMBER = version.__version__
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

# set the paths for autohotkey and git bash
if os.path.isfile('C:/Program Files/Git/git-bash.exe'):
    TERMINAL_PATH_DEFAULT = "C:/Program Files/Git/git-bash.exe"
else:
    TERMINAL_PATH_DEFAULT = ""

if os.path.isfile('C:/Program Files/AutoHotkey/AutoHotkey.exe'):
    AHK_PATH_DEFAULT = "C:/Program Files/AutoHotkey/AutoHotkey.exe"
else:
    AHK_PATH_DEFAULT = ""


def get_platform_information():
    """Return a dictionary containing platform-specific information."""
    import sysconfig
    system_information = {"platform": sysconfig.get_platform()}
    system_information.update({"python version": sys.version_info})
    if sys.platform == "win32":
        system_information.update({"binary path": sys.exec_prefix})
        system_information.update(
            {"main binary": os.path.join(sys.exec_prefix, "python.exe")})
        system_information.update(
            {"hidden console binary": os.path.join(sys.exec_prefix, "pythonw.exe")})
    else:
        system_information.update({"binary path": os.path.join(sys.exec_prefix, "bin")})
        system_information.update(
            {"main binary": os.path.join(sys.exec_prefix, "bin", "python")})
        system_information.update(
            {"hidden console binary": os.path.join(sys.exec_prefix, "bin", "python")})
    return system_information


SYSTEM_INFORMATION = get_platform_information()


def get_filename():
    return _SETTINGS_PATH


def _validate_engine_path():
    '''
    Validates path 'Engine Path' in settings.toml
    '''
    if not sys.platform.startswith('win'):
        return ''
    try:
        # pylint: disable=import-error
        import natlink
    except ImportError:
        return ''
    if os.path.isfile(_SETTINGS_PATH):
        with io.open(_SETTINGS_PATH, "rt", encoding="utf-8") as toml_file:
            data = tomlkit.loads(toml_file.read()).value
            engine_path = data["paths"]["ENGINE_PATH"]
            if os.path.isfile(engine_path):
                return engine_path
            else:
                engine_path = _find_natspeak()
                data["paths"]["ENGINE_PATH"] = engine_path
                try:
                    formatted_data = unicode(tomlkit.dumps(data))
                    with io.open(_SETTINGS_PATH, "w", encoding="utf-8") as toml_file:
                        toml_file.write(formatted_data)
                    print("Setting engine path to " + engine_path)
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
    try:
        proc_arch64 = os.environ['PROCESSOR_ARCHITEW6432'].lower()
    except KeyError:
        proc_arch64 = False

    if proc_arch == 'x86' and not proc_arch64:
        arch_keys = {0}
    elif proc_arch == 'x86' or proc_arch == 'amd64':
        arch_keys = {_winreg.KEY_WOW64_32KEY, _winreg.KEY_WOW64_64KEY}
    else:
        raise Exception("Unhandled arch: %s" % proc_arch)

    for arch_key in arch_keys:
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
                              "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
                              0, _winreg.KEY_READ | arch_key)
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
                            print("Search Complete.")
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
        "BASE_PATH":
            BASE_PATH,
        "USER_DIR":
            _USER_DIR,

        # DATA
        "BRINGME_PATH":
            _USER_DIR + "/data/bringme.toml",
        "BRINGME_DEFAULTS_PATH":
            BASE_PATH + "/bin/share/bringme.toml.defaults",
        "FILTER_RULES_DEFAULTS_PATH":
            BASE_PATH + "/bin/share/FilterRules",
        "RULES_RULES_DEFAULTS_PATH":
            BASE_PATH + "/bin/share/Rules",
        "ALIAS_PATH":
            _USER_DIR + "/data/aliases.toml",
        "CCR_CONFIG_PATH":
            _USER_DIR + "/data/ccr.toml",
        "DLL_PATH":
            BASE_PATH + "/lib/dll/",
        "SIMPLIFIED_FILTER_RULES_PATH":
            _USER_DIR + "/filters/words.txt",
        "LOG_PATH":
            _USER_DIR + "/log.txt",
        "RECORDED_MACROS_PATH":
            _USER_DIR + "/data/recorded_macros.toml",
        "SAVED_CLIPBOARD_PATH":
            _USER_DIR + "/data/clipboard.json",
        "SIKULI_SCRIPTS_PATH":
            _USER_DIR + "/sikuli",
        "GIT_REPO_LOCAL_REMOTE_PATH":
            _USER_DIR + "/data/git_repo_local_to_remote_match.toml",
        "GIT_REPO_LOCAL_REMOTE_DEFAULT_PATH":
            BASE_PATH + "/bin/share/git_repo_local_to_remote_match.toml.defaults",

        # REMOTE_DEBUGGER_PATH is the folder in which pydevd.py can be found
        "REMOTE_DEBUGGER_PATH":
            "",

        # SIKULIX EXECUTABLES
        "SIKULI_IDE":
            "",
        "SIKULI_RUNNER":
            "",

        # EXECUTABLES
        "AHK_PATH":
            AHK_PATH_DEFAULT,
        "DOUGLAS_PATH":
            BASE_PATH + "/asynch/mouse/grids.py",
        "ENGINE_PATH":
            _validate_engine_path(),
        "HOMUNCULUS_PATH":
            BASE_PATH + "/asynch/hmc/h_launch.py",
        "LEGION_PATH":
            BASE_PATH + "/asynch/mouse/legion.py",
        "MEDIA_PATH":
            BASE_PATH + "/bin/media",
        "RAINBOW_PATH":
            BASE_PATH + "/asynch/mouse/grids.py",
        "REBOOT_PATH":
            BASE_PATH + "/bin/reboot.bat",
        "REBOOT_PATH_WSR":
            BASE_PATH + "/bin/reboot_wsr.bat",
        "SETTINGS_WINDOW_PATH":
            BASE_PATH + "/asynch/settingswindow.py",
        "SIKULI_SERVER_PATH":
            BASE_PATH + "/asynch/sikuli/server/xmlrpc_server.sikuli",
        "WSR_PATH":
            "C:/Windows/Speech/Common/sapisvr.exe",
        "TERMINAL_PATH":
            TERMINAL_PATH_DEFAULT,

        # CCR
        "CONFIGDEBUGTXT_PATH":
            _USER_DIR + "/data/configdebug.txt",

        # PYTHON
        "PYTHONW":
            SYSTEM_INFORMATION["hidden console binary"],
    },

    # python settings
    "python": {
        "automatic_settings":
            True,  # Set to false to manually set "version" and "pip" below.
        "version":
            "python",  # Depending Python setup (python, python2, python2.7, py, py -2)
        "pip": "pip"  # Depending on PIP setup (pip ,pip2, pip2.7)
    },

    # sikuli settings
    "sikuli": {
        "enabled": False,
        "version": ""
    },

    # gitbash settings
    "gitbash": {
        "loading_time": 5,  # the time to initialise the git bash window in seconds
        "fetching_time": 3  # the time to fetch a github repository in seconds
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
        "dev_commands": True,
        "keypress_wait": 50,  # milliseconds
        "max_ccr_repetitions": 16,
        "atom_palette_wait": 30,  # hundredths of a second
        "rdp_mode": False,  # Switch app context manually for remote desktop
        "integer_remap_opt_in": False,
        "short_integer_opt_out": False,
        "integer_remap_crash_fix": False,
        "print_rdescripts": True,
        "history_playback_delay_secs": 1.0,
        "legion_vertical_columns": 30,
        "use_aenea": False,
        "online_mode": True,
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
        formatted_data = unicode(tomlkit.dumps(data))
        with io.open(path, "wt", encoding="utf-8") as f:
            f.write(formatted_data)
    except Exception as e:
        print("Error saving toml file: " + str(e) + _SETTINGS_PATH)


def _init(path):
    result = {}
    try:
        with io.open(path, "rt", encoding="utf-8") as f:
            result = tomlkit.loads(f.read()).value
    except ValueError as e:
        print("\n\n" + repr(e) + " while loading settings file: " + path + "\n\n")
        print(sys.exc_info())
    except IOError as e:
        print("\n\n" + repr(e) + " while loading settings file: " + path +
              "\nAttempting to recover...\n\n")
    result, num_default_added = _deep_merge_defaults(result, _DEFAULT_SETTINGS)
    # Temporary piece of code to seamlessly migrate clipboards to JSON
    if result["paths"]["SAVED_CLIPBOARD_PATH"].endswith(".toml"):
        old_clipboard = result["paths"]["SAVED_CLIPBOARD_PATH"]
        import json
        clipboard = {}
        new_path = old_clipboard[:-4] + "json"
        print("\n\n Migrating clipboard from {} to {}".format(old_clipboard, new_path))
        with io.open(old_clipboard, "rt", encoding="utf-8") as f:
            clipboard = tomlkit.loads(f.read()).value
        formatted_data = unicode(json.dumps(clipboard, ensure_ascii=False))
        with io.open(new_path, "wt", encoding="utf-8") as f:
            f.write(formatted_data)
        result["paths"]["SAVED_CLIPBOARD_PATH"] = new_path
        if os.path.exists(old_clipboard):
            os.remove(old_clipboard)
        if not num_default_added:
            _save(result, _SETTINGS_PATH)
    if num_default_added > 0:
        print("Default settings values added: %d " % num_default_added)
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
_debugger_path = SETTINGS["paths"]["REMOTE_DEBUGGER_PATH"]
if _debugger_path not in sys.path and os.path.isdir(_debugger_path):
    sys.path.append(_debugger_path)
