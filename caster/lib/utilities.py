# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import io
import json
import os
import re
import sys
import traceback
from __builtin__ import True
from subprocess import Popen

import win32gui
import win32ui
from dragonfly.windows.window import Window

try:  # Style C -- may be imported into Caster, or externally
    BASE_PATH = os.path.realpath(__file__).split("\\caster")[0].replace("\\", "/")
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
finally:
    from caster.lib import settings

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


def save_json_file(data, path):
    try:
        formatted_data = unicode(
            json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False))
        with io.open(path, "wt", encoding="utf-8") as f:
            f.write(formatted_data)
    except Exception:
        simple_log(True)


def load_json_file(path):
    result = {}
    try:
        with io.open(path, "rt", encoding="utf-8") as f:
            result = json.loads(f.read())
    except IOError as e:
        if e.errno == 2:  # The file doesn't exist.
            save_json_file(result, path)
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
        import pydevd  # @UnresolvedImport
        pydevd.settrace()
    except Exception:
        print("ERROR: " + who_called_it +
              " called utilities.remote_debug() but the debug server wasn't running.")


def reboot(wsr=False):
    popen_parameters = []
    if wsr:
        popen_parameters.append(settings.SETTINGS["paths"]["REBOOT_PATH_WSR"])
        popen_parameters.append(settings.SETTINGS["paths"]["WSR_PATH"])
        # caster path inserted too if there's a way to wake up WSR
    else:
        popen_parameters.append(settings.SETTINGS["paths"]["REBOOT_PATH"])
        popen_parameters.append(settings.SETTINGS["paths"]["ENGINE_PATH"])

    print(popen_parameters)
    Popen(popen_parameters)


def command_or_key_nexus(
        key="", cmd=""):  #  Checks to send an API command or send dragonfly key actions
    # Only use dragonfly key actions or an API Commands. API Commands can be combined with dragonfly methods.
    # api = settings.SETTINGS["feature_rules"]["caster_api"]
    debug_api = settings.SETTINGS["feature_rules"]["caster_api_debug"]
    commands_list = cmd
    shortcuts = key
    if debug_api is True:  # If the API is enabled and a String is present send_json_commands will initialize.
        if cmd == "":
            print("The command does not have API implemented")
        else:  # sends json commands
            print("command_key_nexis Initialized to send json commands(cmd)")  # Debugging
            try:  # when post to API fails to send command use keyboard shortcut instead.
                commands_list = map(
                    string.strip, commands_list.split(',')
                )  # from commands_list split strings separated by a comma and removes white spaces.
                for a_command in commands_list:  # for each command found in commands_list post a request to API
                    r = requests.post('http://127.0.0.1:1781/api/commands/' + a_command)
                    r.raise_for_status()
            except requests.exceptions.HTTPError as error:
                print(error)
            except requests.exceptions.RequestException as error:
                Key(shortcuts).execute()
                print(error)
    else:  #
        if shortcuts == "":
            print("The command does not have keyboard shortcut assigned")
        else:
            print("command_key_nexis Initialized Key(shortcuts).execute()")  # Debugging
            Key(shortcuts).execute()