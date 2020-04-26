# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from builtins import str

import collections
import io
import os
import sys
import tomlkit
from past.builtins import xrange

from castervoice.lib import printer
from castervoice.lib import version
from castervoice.lib.util import guidance

from appdirs import *

import six
if six.PY2:
    from castervoice.lib.util.pathlib import Path
else:
    from pathlib import Path  # pylint: disable=import-error

# consts: some of these can easily be moved out of this file
GENERIC_HELP_MESSAGE = """
If you continue having problems with this or any other issue you can contact
us through Gitter at <https://gitter.im/dictation-toolbox/Caster> or on our GitHub
issue tracker at <https://github.com/dictation-toolbox/Caster/issues>.
Thank you for using Caster!
"""
SOFTWARE_VERSION_NUMBER = version.__version__
SOFTWARE_NAME = "Caster v " + SOFTWARE_VERSION_NUMBER
HOMUNCULUS_VERSION = "HMC v " + SOFTWARE_VERSION_NUMBER
HMC_TITLE_RECORDING = " :: Recording Manager"
HMC_TITLE_DIRECTORY = " :: Directory Selector"
HMC_TITLE_CONFIRM = " :: Confirm"
LEGION_TITLE = "legiongrid"
RAINBOW_TITLE = "rainbowgrid"
DOUGLAS_TITLE = "douglasgrid"
SUDOKU_TITLE = "sudokugrid"
SETTINGS_WINDOW_TITLE = "Caster Settings Window v "
QTYPE_DEFAULT = "0"
QTYPE_INSTRUCTIONS = "3"
QTYPE_RECORDING = "4"
QTYPE_DIRECTORY = "5"
QTYPE_CONFIRM = "6"
WXTYPE_SETTINGS = "7"
HMC_SEPARATOR = "[hmc]"

# calculated fields
SETTINGS = None
SYSTEM_INFORMATION = None
WSR = False
_BASE_PATH = None
_USER_DIR = None
_SETTINGS_PATH = None


def _get_platform_information():
    """Return a dictionary containing platform-specific information."""
    import sysconfig
    system_information = {"platform": sysconfig.get_platform()}
    system_information.update({"python version": sys.version_info})
    if sys.platform == "win32":
        system_information.update({"binary path": sys.exec_prefix})
        system_information.update(
            {"main binary": str(Path(sys.exec_prefix).joinpath("python.exe"))})
        system_information.update(
            {"hidden console binary": str(Path(sys.exec_prefix).joinpath("pythonw.exe"))})
    else:
        system_information.update({"binary path": str(Path(sys.exec_prefix).joinpath(sys.exec_prefix).joinpath("bin"))})
        system_information.update(
            {"main binary": str(Path(sys.exec_prefix).joinpath("bin", "python"))})
        system_information.update(
            {"hidden console binary": str(Path(sys.exec_prefix).joinpath("bin", "python"))})
    return system_information


def get_filename():
    return _SETTINGS_PATH


def _validate_engine_path():
    '''
    Validates path 'Engine Path' in settings.toml
    '''
    if not sys.platform.startswith('win'):
        return ''
    try:
        import natlink  # pylint: disable=import-error
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
                    formatted_data = str(tomlkit.dumps(data))
                    with io.open(_SETTINGS_PATH, "w", encoding="utf-8") as toml_file:
                        toml_file.write(formatted_data)
                    printer.out("Setting engine path to {}".format(engine_path))
                except Exception as e:
                    printer.out("Error saving settings file {} {} ".format(e, _SETTINGS_PATH))
                return engine_path
    else:
        return _find_natspeak()


def _find_natspeak():
    '''
    Finds engine 'natspeak.exe' path and verifies supported DNS versions via Windows Registry.
    '''

    try:
        if six.PY2:
            import _winreg as winreg
        else:
            import winreg
    except ImportError:
        printer.out("Could not import winreg")
        return ""

    printer.out("Searching Windows Registry For DNS...")
    proc_arch = os.environ['PROCESSOR_ARCHITECTURE'].lower()
    try:
        proc_arch64 = os.environ['PROCESSOR_ARCHITEW6432'].lower()
    except KeyError:
        proc_arch64 = False

    if proc_arch == 'x86' and not proc_arch64:
        arch_keys = {0}
    elif proc_arch == 'x86' or proc_arch == 'amd64':
        arch_keys = {winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY}
    else:
        raise Exception("Unhandled arch: %s" % proc_arch)

    for arch_key in arch_keys:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
                             0, winreg.KEY_READ | arch_key)
        for i in xrange(0, winreg.QueryInfoKey(key)[0]):
            skey_name = winreg.EnumKey(key, i)
            skey = winreg.OpenKey(key, skey_name)
            DisplayName, Publisher, DisplayVersion, InstallLocation = 'null'
            try:
                DisplayName = winreg.QueryValueEx(skey, 'DisplayName')[0]
                Publisher = winreg.QueryValueEx(skey, 'Publisher')[0]
                DisplayVersion = winreg.QueryValueEx(skey, 'DisplayVersion')[0]
                InstallLocation = winreg.QueryValueEx(skey, 'InstallLocation')[0]
            except OSError as error:
                if error.errno == 2:  # Suppresses '[Error 2] The system cannot find the file specified'
                    pass
                else:
                    printer.out(error)
            finally:
                skey.Close()
                if Publisher == "Nuance Communications Inc." and "Dragon" in DisplayName:
                    DnsVersion = int(str(DisplayVersion)[:2])
                    if DnsVersion >= 13:
                        engine_path = str(Path(InstallLocation).joinpath("Program/natspeak.exe"))
                        if os.path.isfile(engine_path):
                            printer.out("Search Complete.")
                            return engine_path
                    else:
                        printer.out(
                            "Dragon Naturally Speaking {} is not supported by Caster. Only versions 13 and above are supported. Purchase Dragon Naturally Speaking 13 or above"
                            .format(DnsVersion))
    printer.out("Cannot find dragon engine path")
    return ""


def _save(data, path):
    """
    Only to be used for settings file.
    :param data:
    :param path:
    :return:
    """
    guidance.offer()
    try:
        formatted_data = str(tomlkit.dumps(data))
        with io.open(path, "wt", encoding="utf-8") as f:
            f.write(formatted_data)
    except Exception as e:
        printer.out("Error saving toml file: {} {}".format(e, _SETTINGS_PATH))


def _init(path):
    guidance.offer()
    result = {}
    try:
        with io.open(path, "rt", encoding="utf-8") as f:
            result = tomlkit.loads(f.read()).value
    except ValueError as e:
        printer.out("\n\n {} while loading settings file: {} \n\n".format(repr(e), path))
        printer.out(sys.exc_info())
    except IOError as e:
        printer.out("\n\n {} while loading settings file: {} \nAttempting to recover...\n\n".format(repr(e), path))
    default_settings = _get_defaults()
    result, num_default_added = _deep_merge_defaults(result, default_settings)
    if num_default_added > 0:
        printer.out("Default settings values added: {} ".format(num_default_added))
        _save(result, _SETTINGS_PATH)
    return result


def _deep_merge_defaults(data, defaults):
    """
    Recursivly merge data and defaults, preferring data.
    Only handles nested dicts and scalar values.
    Modifies `data` in place.
    """
    changes = 0
    for key, default_value in defaults.items():
        # If the key is in the data, use that, but call recursivly if it's a dict.
        if key in data:
            if isinstance(data[key], collections.Mapping):
                child_data, child_changes = _deep_merge_defaults(data[key], default_value)
                data[key] = child_data
                changes += child_changes
        else:
            data[key] = default_value
            changes += 1
    return data, changes


def _get_defaults():
    terminal_path_default = "C:/Program Files/Git/git-bash.exe"
    if not os.path.isfile(terminal_path_default):
        terminal_path_default = ""

    ahk_path_default = "C:/Program Files/AutoHotkey/AutoHotkey.exe"
    if not os.path.isfile(ahk_path_default):
        ahk_path_default = ""

    return {
        "paths": {
            "BASE_PATH":
                _BASE_PATH,
            "USER_DIR":
                _USER_DIR,
            # pathlib string conversion can be removed once pathlib is utilized throughout Caster.
            # DATA
            "SM_BRINGME_PATH":
                str(Path(_USER_DIR).joinpath("settings/sm_bringme.toml")),
            "SM_ALIAS_PATH":
                str(Path(_USER_DIR).joinpath("data/sm_aliases.toml")),
            "SM_CHAIN_ALIAS_PATH":
                str(Path(_USER_DIR).joinpath("data/sm_chain_aliases.toml")),
            "SM_HISTORY_PATH":
                str(Path(_USER_DIR).joinpath("data/sm_history.toml")),
            "RULES_CONFIG_PATH":
                str(Path(_USER_DIR).joinpath("settings/rules.toml")),
            "TRANSFORMERS_CONFIG_PATH":
                str(Path(_USER_DIR).joinpath("settings/transformers.toml")),
            "HOOKS_CONFIG_PATH":
                str(Path(_USER_DIR).joinpath("settings/hooks.toml")),
            "COMPANION_CONFIG_PATH":
                str(Path(_USER_DIR).joinpath("settings/companion_config.toml")),
            "DLL_PATH":
                str(Path(_BASE_PATH).joinpath("lib/dll/")),
            "GDEF_FILE":
                str(Path(_USER_DIR).joinpath("transformers/words.txt")),
            "LOG_PATH":
                str(Path(_USER_DIR).joinpath("log.txt")),
            "SAVED_CLIPBOARD_PATH":
                str(Path(_USER_DIR).joinpath("data/clipboard.json")),
            "SIKULI_SCRIPTS_PATH":
                str(Path(_USER_DIR).joinpath("sikuli")),
            "GIT_REPO_LOCAL_REMOTE_PATH":
                str(Path(_USER_DIR).joinpath("settings/git_repo_local_to_remote_match.toml")),
            "GIT_REPO_LOCAL_REMOTE_DEFAULT_PATH":
                str(Path(_BASE_PATH).joinpath("bin/share/git_repo_local_to_remote_match.toml.defaults")),

            # REMOTE_DEBUGGER_PATH is the folder in which pydevd.py can be found
            "REMOTE_DEBUGGER_PATH":
                str(Path("")),

            # SIKULIX EXECUTABLES
            "SIKULI_IDE":
                str(Path("")),
            "SIKULI_RUNNER":
                str(Path("")),

            # EXECUTABLES
            "AHK_PATH":
                str(Path(_BASE_PATH).joinpath(ahk_path_default)),
            "DOUGLAS_PATH":
                str(Path(_BASE_PATH).joinpath("asynch/mouse/grids.py")),
            "ENGINE_PATH":
                _validate_engine_path(),
            "HOMUNCULUS_PATH":
                str(Path(_BASE_PATH).joinpath("asynch/hmc/h_launch.py")),
            "LEGION_PATH":
                str(Path(_BASE_PATH).joinpath("asynch/mouse/legion.py")),
            "MEDIA_PATH":
                str(Path(_BASE_PATH).joinpath("bin/media")),
            "RAINBOW_PATH":
                str(Path(_BASE_PATH).joinpath("asynch/mouse/grids.py")),
            "REBOOT_PATH":
                str(Path(_BASE_PATH).joinpath("bin/reboot.bat")),
            "REBOOT_PATH_WSR":
                str(Path(_BASE_PATH).joinpath("bin/reboot_wsr.bat")),
            "SETTINGS_WINDOW_PATH":
                str(Path(_BASE_PATH).joinpath("asynch/settingswindow.py")),
            "SIKULI_SERVER_PATH":
                str(Path(_BASE_PATH).joinpath("asynch/sikuli/server/xmlrpc_server.sikuli")),
            "SUDOKU_PATH":
                str(Path(_BASE_PATH).joinpath("asynch/mouse/grids.py")),
            "WSR_PATH":
                str(Path(_BASE_PATH).joinpath("C:/Windows/Speech/Common/sapisvr.exe")),
            "TERMINAL_PATH":
                str(Path(terminal_path_default)),

            # CCR
            "CONFIGDEBUGTXT_PATH":
                str(Path(_USER_DIR).joinpath("data/configdebug.txt")),

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

        # node rules path
        "Tree_Node_Path": {
            "SM_CSS_TREE_PATH": str(Path(_USER_DIR).joinpath("data/sm_css_tree.toml")),
        },

        "online": {
            "online_mode": True,  # False disables updates
            "last_update_date": "None",
            "update_interval": 7  # Days
        },

        # Default enabled hooks: Use hook class name
        "hooks": {
            "default_hooks": ['PrinterHook'],
        },

        # miscellaneous section
        "miscellaneous": {
            "dev_commands": True,
            "keypress_wait": 50,  # milliseconds
            "max_ccr_repetitions": 16,
            "atom_palette_wait": 30,  # hundredths of a second
            "integer_remap_opt_in": False,
            "short_integer_opt_out": False,
            "integer_remap_crash_fix": False,
            "print_rdescripts": True,
            "history_playback_delay_secs": 1.0,
            "legion_vertical_columns": 30,
            "legion_downscale_factor": "auto",
            "use_aenea": False,
            "hmc": True,
            "ccr_on": True,
            "dragonfly_pause_default":  0.003,  # dragonfly _pause_default 0.02 is too slow! Caster default 0.003
        },
        # Grammar reloading section
        "grammar_reloading": {
            "reload_trigger": "timer",  # manual or timer
            "reload_timer_seconds": 5,  # seconds
        },

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


def settings(key_path, default_value=None):
    """
    This should be the preferred way to use settings.SETTINGS,
    a KeyError-safe function call to access the settings dict.
    """
    dv = False if default_value is None else default_value
    if SETTINGS is None:
        return dv
    value = SETTINGS
    for k in key_path:
        if k in value:
            value = value[k]
        else:
            return dv
    return value


def save_config():
    """
    Save the current in-memory settings to disk
    """
    _save(SETTINGS, _SETTINGS_PATH)


def initialize():
    global SETTINGS, SYSTEM_INFORMATION
    global _BASE_PATH, _USER_DIR, _SETTINGS_PATH

    if SETTINGS is not None:
        return

    # calculate prerequisites
    SYSTEM_INFORMATION = _get_platform_information()
    _BASE_PATH = str(Path(__file__).resolve().parent.parent)
    _USER_DIR = user_data_dir(appname="caster", appauthor=False)
    _SETTINGS_PATH = str(Path(_USER_DIR).joinpath("settings/settings.toml"))

    for directory in ["data", "rules", "transformers", "hooks", "sikuli", "settings"]:
        d = Path(_USER_DIR).joinpath(directory)
        d.mkdir(parents=True, exist_ok=True)
    # Kick everything off.
    SETTINGS = _init(_SETTINGS_PATH)
    _debugger_path = SETTINGS["paths"]["REMOTE_DEBUGGER_PATH"]  # pylint: disable=invalid-sequence-index
    if _debugger_path not in sys.path and os.path.isdir(_debugger_path):
        sys.path.append(_debugger_path)
    printer.out("Caster User Directory: {}".format(_USER_DIR))
