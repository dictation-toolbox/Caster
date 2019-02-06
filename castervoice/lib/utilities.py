# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import io
import os
import re
import sys
import traceback
from __builtin__ import True
from subprocess import Popen
import toml

import win32gui
import win32ui

from _winreg import (CloseKey, ConnectRegistry, HKEY_CLASSES_ROOT,
    HKEY_CURRENT_USER, OpenKey, QueryValueEx)

from dragonfly.windows.window import Window

try:  # Style C -- may be imported into Caster, or externally
    BASE_PATH = os.path.realpath(__file__).rsplit(os.path.sep + "castervoice", 1)[0]
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
finally:
    from castervoice.lib import settings

# filename_pattern was used to determine when to update the list in the element window,
# checked to see when a new file name had appeared
FILENAME_PATTERN = re.compile(r"[/\\]([\w_ ]+\.[\w]+)")


def window_exists(classname, windowname):
    try:
        win32ui.FindWindow(classname, windowname)
    except win32ui.error:
        return False
    else:
        return True


def get_active_window_title(pid=None):
    _pid = win32gui.GetForegroundWindow() if pid is None else pid
    return unicode(win32gui.GetWindowText(_pid), errors='ignore')


def get_active_window_path():
    return Window.get_foreground().executable


def get_window_by_title(title):
    # returns 0 if nothing found
    hwnd = win32gui.FindWindowEx(0, 0, 0, title)
    return hwnd


def get_window_title_info():
    '''get name of active file and folders in path;
    will be needed to look up collection of symbols
    in scanner data'''
    global FILENAME_PATTERN
    title = get_active_window_title().replace("\\", "/")
    match_object = FILENAME_PATTERN.findall(title)
    filename = None
    if len(match_object) > 0:
        filename = match_object[0]
    path_folders = title.split("/")[:-1]
    return [filename, path_folders, title]


def save_toml_file(data, path):
    try:
        formatted_data = unicode(toml.dumps(data))
        with io.open(path, "wt", encoding="utf-8") as f:
            f.write(formatted_data)
    except Exception:
        simple_log(True)


def load_toml_file(path):
    result = {}
    try:
        with io.open(path, "rt", encoding="utf-8") as f:
            result = toml.loads(f.read())
    except IOError as e:
        if e.errno == 2:  # The file doesn't exist.
            save_toml_file(result, path)
        else:
            raise
    except Exception:
        simple_log(True)
    return result


def list_to_string(l):
    return u"\n".join([unicode(x) for x in l])


def simple_log(to_file=False):
    msg = list_to_string(sys.exc_info())
    print(msg)
    for tb in traceback.format_tb(sys.exc_info()[2]):
        print(tb)
    if to_file:
        with io.open(settings.SETTINGS["paths"]["LOG_PATH"], 'at', encoding="utf-8") as f:
            f.write(msg + "\n")


def availability_message(feature, dependency):
    print(feature + " feature not available without " + dependency)


def remote_debug(who_called_it=None):
    if who_called_it is None:
        who_called_it = "An unidentified process"
    try:
        import pydevd  # @UnresolvedImport pylint: disable=import-error
        pydevd.settrace()
    except Exception:
        print("ERROR: " + who_called_it +
              " called utilities.remote_debug() but the debug server wasn't running.")


def reboot(wsr=False):
    popen_parameters = []
    if wsr:
        popen_parameters.append(settings.SETTINGS["paths"]["REBOOT_PATH_WSR"])
        popen_parameters.append(settings.SETTINGS["paths"]["WSR_PATH"])
        # castervoice path inserted too if there's a way to wake up WSR
    else:
        popen_parameters.append(settings.SETTINGS["paths"]["REBOOT_PATH"])
        popen_parameters.append(settings.SETTINGS["paths"]["ENGINE_PATH"])

    print(popen_parameters)
    Popen(popen_parameters)

def default_browser_command():
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
    except WindowsError as e:
        #logger.warn(e)
        return ''
    finally:
        CloseKey(key)
        CloseKey(reg)
    return path
