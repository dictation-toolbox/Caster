# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from builtins import str

import io
import json
import locale
import six
import os
import re
import sys
import six
import time
import traceback
from subprocess import Popen
import tomlkit

from dragonfly import Key, Pause, Window, get_current_engine

from castervoice.lib.clipboard import Clipboard
from castervoice.lib import printer
from castervoice.lib.util import guidance

if six.PY2:
    from castervoice.lib.util.pathlib import Path
else:
    from pathlib import Path  # pylint: disable=import-error

try:  # Style C -- may be imported into Caster, or externally
    BASE_PATH = str(Path(__file__).resolve().parent.parent)
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
finally:
    from castervoice.lib import settings, printer


# TODO: Move functions that manipulate or retrieve information from Windows to `window_mgmt_support` in navigation_rules.
# TODO: Implement Optional exact title matching for `get_matching_windows` in Dragonfly
def window_exists(windowname=None, executable=None):
    if Window.get_matching_windows(title=windowname, executable=executable):
        return True
    else:
        return False


def get_window_by_title(title=None): 
    # returns 0 if nothing found
    Matches = Window.get_matching_windows(title=title)
    if Matches:
        return Matches[0].handle
    else:
        return 0 


def get_active_window_title():
    return Window.get_foreground().title


def get_active_window_path():
    return Window.get_foreground().executable


def get_active_window_info():
    '''Returns foreground window executable_file, executable_path, title, handle, classname'''
    FILENAME_PATTERN = re.compile(r"[/\\]([\w_ ]+\.[\w]+)")
    window = Window.get_foreground()
    executable_path = str(Path(get_active_window_path()))
    match_object = FILENAME_PATTERN.findall(window.executable)
    executable_file = None
    if len(match_object) > 0:
        executable_file = match_object[0]
    return [executable_file, executable_path, window.title, window.handle, window.classname]


def maximize_window():
    '''
    Maximize foreground Window
    '''
    Window.get_foreground().maximize()


def minimize_window():
    '''
    Minimize foreground Window
    '''
    Window.get_foreground().minimize()


def focus_mousegrid(gridtitle):
    '''
    Loops over active windows for MouseGrid window titles. Issue #171
    When MouseGrid window titles found focuses MouseGrid overly.
    '''
    if sys.platform.startswith('win'):
        # May not be needed for Linux/Mac OS - testing required
        try:
            for i in range(9):
                matches = Window.get_matching_windows(title=gridtitle, executable="python")
                if not matches:
                    Pause("50").execute()
                else:
                    break
            if matches:
                for handle in matches:
                    handle.set_foreground()
                    break
            else:
                printer.out("`Title: `{}` no matching windows found".format(gridtitle))
        except Exception as e:
            printer.out("Error focusing MouseGrid: {}".format(e))
    else:
        pass


def save_toml_file(data, path):
    guidance.offer()
    try:
        formatted_data = str(tomlkit.dumps(data))
        with io.open(path, "wt", encoding="utf-8") as f:
            f.write(formatted_data)
    except Exception:
        simple_log(True)


def load_toml_file(path):
    guidance.offer()
    result = {}
    try:
        with io.open(path, "rt", encoding="utf-8") as f:
            result = tomlkit.loads(f.read()).value
    except IOError as e:
        if e.errno == 2:  # The file doesn't exist.
            save_toml_file(result, path)
        else:
            raise
    except Exception:
        simple_log(True)
    return result


def save_json_file(data, path):
    guidance.offer()
    try:
        formatted_data = str(json.dumps(data, ensure_ascii=False))
        with io.open(path, "wt", encoding="utf-8") as f:
            f.write(formatted_data)
    except Exception:
        simple_log(True)


def load_json_file(path):
    guidance.offer()
    result = {}
    try:
        with io.open(path, "rt", encoding="utf-8") as json_file:
            result = json.load(json_file)
    except IOError as e:
        if e.errno == 2:  # The file doesn't exist.
            save_json_file(result, path)
        else:
            raise
    except Exception:
        simple_log(True)
    return result


def list_to_string(l):
    return u"\n".join([str(x) for x in l])


def simple_log(to_file=False):
    msg = list_to_string(sys.exc_info())
    printer.out(msg)
    for tb in traceback.format_tb(sys.exc_info()[2]):
        printer.out(tb)
    if to_file:
        with io.open(settings.SETTINGS["paths"]["LOG_PATH"], 'at', encoding="utf-8") as f:
            f.write(msg + "\n")


def availability_message(feature, dependency):
    printer.out(feature + " feature not available without " + dependency)


def remote_debug(who_called_it=None):
    if who_called_it is None:
        who_called_it = "An unidentified process"
    try:
        import pydevd  # @UnresolvedImport pylint: disable=import-error
        pydevd.settrace()
    except Exception:
        printer.out("ERROR: " + who_called_it +
              " called utilities.remote_debug() but the debug server wasn't running.")

def reboot():
    # TODO: Save engine arguments elsewhere and retrieves for reboot. Allows for user-defined arguments.
    popen_parameters = []
    engine = get_current_engine()
    if engine.name == 'kaldi':
        engine.disconnect()
        Popen([sys.executable, '-m', 'dragonfly', 'load', '_*.py', '--engine', 'kaldi',  '--no-recobs-messages'])
    if engine.name == 'sapi5inproc':
        engine.disconnect()
        Popen([sys.executable, '-m', 'dragonfly', 'load', '--engine', 'sapi5inproc', '_*.py', '--no-recobs-messages'])
    if engine.name in ["sapi5shared", "sapi5"]:
        popen_parameters.append(settings.SETTINGS["paths"]["REBOOT_PATH_WSR"])
        popen_parameters.append(settings.SETTINGS["paths"]["WSR_PATH"])
        printer.out(popen_parameters)
        Popen(popen_parameters)
    if engine.name == 'natlink':
        import natlinkstatus # pylint: disable=import-error
        status = natlinkstatus.NatlinkStatus()
        if status.NatlinkIsEnabled() == 1:
            # Natlink in-process
            popen_parameters.append(settings.SETTINGS["paths"]["REBOOT_PATH"])
            popen_parameters.append(settings.SETTINGS["paths"]["ENGINE_PATH"])
            username = status.getUserName()
            popen_parameters.append(username)
            printer.out(popen_parameters)
            Popen(popen_parameters)
        else:
           # Natlink out-of-process
            engine.disconnect()
            Popen([sys.executable, '-m', 'dragonfly', 'load', '--engine', 'natlink', '_*.py', '--no-recobs-messages'])


# TODO: Implement default_browser_command Mac/Linux
def default_browser_command():
    if sys.platform.startswith('win'):
        if six.PY2:
            from _winreg import (CloseKey, ConnectRegistry, HKEY_CLASSES_ROOT, # pylint: disable=import-error,no-name-in-module
                        HKEY_CURRENT_USER, OpenKey, QueryValueEx)
        else:
            from winreg import (CloseKey, ConnectRegistry, HKEY_CLASSES_ROOT, # pylint: disable=import-error,no-name-in-module
                        HKEY_CURRENT_USER, OpenKey, QueryValueEx)
        '''
        Tries to get default browser command, returns either a space delimited
        command string with '%1' as URL placeholder, or empty string.
        '''
        browser_class = 'Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\https\\UserChoice'
        try:
            reg = ConnectRegistry(None,HKEY_CURRENT_USER)
            key = OpenKey(reg, browser_class)
            value, t = QueryValueEx(key, 'ProgId')
            CloseKey(key)
            CloseKey(reg)
            reg = ConnectRegistry(None,HKEY_CLASSES_ROOT)
            key = OpenKey(reg, '%s\\shell\\open\\command' % value)
            path, t = QueryValueEx(key, None)
        except WindowsError:  # pylint: disable=undefined-variable
            # logger.warn(e)
            traceback.print_exc()
            return ''
        finally:
            CloseKey(key)
            CloseKey(reg)
        return path
    else:
        printer.out("default_browser_command: Not implemented for OS")


def clear_log():
    # Function to clear status window.
    # Natlink status window not used an out-of-process mode.
    # TODO: window_exists utilized when engine launched through Dragonfly CLI via bat in future
    try:
        if sys.platform.startswith('win'):
            clearcmd = "cls" # Windows OS
        else:
            clearcmd = "clear" # Linux
        if get_current_engine().name == 'natlink':
            import natlinkstatus  # pylint: disable=import-error
            status = natlinkstatus.NatlinkStatus()
            if status.NatlinkIsEnabled() == 1:
                import win32gui  # pylint: disable=import-error
                handle = get_window_by_title("Messages from Python Macros") or get_window_by_title("Messages from Natlink")
                rt_handle = win32gui.FindWindowEx(handle, None, "RICHEDIT", None)
                win32gui.SetWindowText(rt_handle, "")
            else:
                if window_exists(windowname="Caster: Status Window"):
                    os.system(clearcmd)
        else:
            if window_exists(windowname="Caster: Status Window"):
                os.system(clearcmd)
            else:
                printer.out("clear_log: Not implemented with GUI")
    except Exception as e:
        printer.out(e)


# TODO: BringMe - Implement clipboard formats for Mac/Linux
def get_clipboard_formats():
    '''
    Return list of all data formats currently in the clipboard
    '''
    formats = []
    if sys.platform.startswith('win'):
        import win32clipboard  # pylint: disable=import-error
        f = win32clipboard.EnumClipboardFormats(0)
        while f:
            formats.append(f)
            f = win32clipboard.EnumClipboardFormats(f)
        return formats
    else:
        printer.out("get_clipboard_formats: Not implemented for OS")


def get_selected_files(folders=False):
    '''
    Copy selected (text or file is subsequently of interest) to a fresh clipboard
    '''
    if sys.platform.startswith('win'):
        cb = Clipboard(from_system=True)
        cb.clear_clipboard()
        Key("c-c").execute()
        time.sleep(0.1)
        files = get_clipboard_files(folders)
        cb.copy_to_system()
        return files
    else:
        printer.out("get_selected_files: Not implemented for OS")


def get_clipboard_files(folders=False):
    '''
    Enumerate clipboard content and return files either directly copied or
    highlighted path copied
    '''
    if sys.platform.startswith('win'):
        import win32clipboard  # pylint: disable=import-error
        files = None
        win32clipboard.OpenClipboard()
        f = get_clipboard_formats()
        if win32clipboard.CF_HDROP in f:
            files = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
        elif win32clipboard.CF_UNICODETEXT in f:
            files = [win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)]
        elif win32clipboard.CF_TEXT in f:
            files = [win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)]
        elif win32clipboard.CF_OEMTEXT in f:
            files = [win32clipboard.GetClipboardData(win32clipboard.CF_OEMTEXT)]
        if folders:
            files = [f for f in files if os.path.isdir(f)] if files else None
        else:
            files = [f for f in files if os.path.isfile(f)] if files else None
        win32clipboard.CloseClipboard()
        return files
    else:
        printer.out("get_clipboard_files: Not implemented for OS")
