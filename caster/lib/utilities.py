# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
import multiprocessing
import os, json, sys
import re
from subprocess import Popen

import win32com.client
import win32gui, win32ui


try: # Style C -- may be imported into Caster, or externally
    BASE_PATH = "C:/NatLink/NatLink/MacroSystem/"
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

def focus_window(pid=None, title=None):
    if pid == None and title == None:
        return
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.AppActivate(pid if pid != None else title)

def get_active_window_hwnd():
    return str(win32gui.GetForegroundWindow())

def get_active_window_title(p=None):
    pid=win32gui.GetForegroundWindow() if p==None else p
    return unicode(win32gui.GetWindowText(pid), errors='ignore')

def get_active_window_path(natlink):
    return natlink.getCurrentModule()[0]

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

def clear_pyc():
    try:
        for dirpath, dirnames, files in os.walk(settings.SETTINGS["paths"]["BASE_PATH"]):  # os.walk produces a list of 3-tuples
            if r"MacroSystem\.git" in dirpath or r"MacroSystem\core" in dirpath:
                continue
            for f in files:
                if f.endswith(".pyc"):
                    f = os.path.join(dirpath, f)
                    os.remove(f)
    except Exception:
        simple_log(True)

def get_most_recent(path, extension):
    recent = 0
    for f in os.listdir(path):
        if f.endswith(extension):
            cur = int(f)
            if cur > recent:
                recent = cur
    if recent == 0:
        return None
    return str(recent) + extension

def clean_temporary_files():
    temp_folders = []
    for p in temp_folders:
        if os.path.exists(p):
            for f in os.listdir(p):
                os.remove(p + f)
                





def list_to_string(l):
    return "\n".join([str(x) for x in l])
            
def simple_log(to_file=False):
    msg = list_to_string(sys.exc_info())
    print msg
    if to_file:
        f = open(settings.SETTINGS["paths"]["LOG_PATH"], 'a') 
        f.write(msg + "\n")
        f.close()




def report(message, speak=False, console=True, log=False):
    import dragonfly
    if console:
        print message
    if speak:
        dragonfly.get_engine().speak(message)
    if log:
        settings.report_to_file(message)

def availability_message(feature, dependency):
    report(feature + " feature not available without " + dependency)




# end stuff that was moved
def remote_debug(who_called_it=None):
    import pydevd;  # @UnresolvedImport
    if who_called_it == None:
        who_called_it = "An unidentified process"
    try:
        pydevd.settrace()
    except Exception:
        print "ERROR: " + who_called_it + " called utilities.remote_debug() but the debug server wasn't running."
    


def current_time_to_string():
    return datetime.now().strftime("%Y%m%d%H%M%S")



def run_in_separate_thread(func, timeout_in_seconds=300):
    p = multiprocessing.Process(target=func)
    p.start()
    p.join(timeout_in_seconds)

    if p.is_alive():
        p.terminate()
        p.join()

def reboot():
    print [settings.SETTINGS["paths"]["REBOOT_PATH"], "\""+settings.SETTINGS["paths"]["ENGINE_PATH"]+"\""]
    Popen([settings.SETTINGS["paths"]["REBOOT_PATH"], settings.SETTINGS["paths"]["ENGINE_PATH"]])


