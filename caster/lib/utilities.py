# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, json, sys
import re
from subprocess import Popen
import traceback

from dragonfly.windows.window import Window
import win32gui, win32ui


try: # Style C -- may be imported into Caster, or externally
    BASE_PATH = os.path.realpath(__file__).split("\\caster")[0].replace("\\", "/")
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
finally:
    from caster.lib import settings

# filename_pattern was used to determine when to update the list in the element window, checked to see when a new file name had appeared
FILENAME_PATTERN = re.compile(r"[/\\]([\w_ ]+\.[\w]+)")

def window_exists(classname, windowname):
    try:
        win32ui.FindWindow(classname, windowname)
    except win32ui.error:
        return False
    else:
        return True

def get_active_window_title(pid=None):
    _pid=win32gui.GetForegroundWindow() if pid is None else pid
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
    


# begin stuff that was moved

def save_json_file(data, path):
    try:
        formatted_data = json.dumps(data, sort_keys=True, indent=4,
            ensure_ascii=False)
        if not os.path.exists(path):
            f = open(path, "w")
            f.close()
        with open(path, "w") as f:
            f.write(formatted_data)
    except Exception:
        simple_log(True)

def load_json_file(path):
    result = {}
    try:
        if os.path.isfile(path):  # If the file exists.
            with open(path, "r") as f:
                result = json.loads(f.read())
                f.close()
        else:
            save_json_file(result, path)
    except Exception:
        simple_log(True)
    return result


def list_to_string(l):
    return "\n".join([str(x) for x in l])
            
def simple_log(to_file=False):
    msg = list_to_string(sys.exc_info())
    print(msg)
    for tb in traceback.format_tb(sys.exc_info()[2]):
        print(tb)
    if to_file:
        f = open(settings.SETTINGS["paths"]["LOG_PATH"], 'a') 
        f.write(msg + "\n")
        f.close()



def availability_message(feature, dependency):
    print(feature + " feature not available without " + dependency)

# end stuff that was moved
def remote_debug(who_called_it=None):
    import pydevd;  # @UnresolvedImport
    if who_called_it is None:
        who_called_it = "An unidentified process"
    try:
        pydevd.settrace()
    except Exception:
        print("ERROR: " + who_called_it + " called utilities.remote_debug() but the debug server wasn't running.")
    

def launch_status():
    if not window_exists(None, settings.STATUS_WINDOW_TITLE):
        Popen(["pythonw", settings.SETTINGS["paths"]["STATUS_WINDOW_PATH"]])

def reboot(wsr=False):
    popen_parameters = []
    if wsr:
        popen_parameters.append(settings.SETTINGS["paths"]["REBOOT_PATH_WSR"])
        popen_parameters.append(settings.SETTINGS["paths"]["WSR_PATH"])
        #caster path inserted too if there's a way to wake up WSR
    else:
        popen_parameters.append(settings.SETTINGS["paths"]["REBOOT_PATH"])
        popen_parameters.append(settings.SETTINGS["paths"]["ENGINE_PATH"])
        
    print(popen_parameters)
    Popen(popen_parameters)


