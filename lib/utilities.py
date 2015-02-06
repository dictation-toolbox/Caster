# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os, json, sys


BASE_PATH = r"C:\NatLink\NatLink\MacroSystem"
if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)
from datetime import datetime
import multiprocessing


from dragonfly import Key
import win32gui, win32process, win32api, win32ui
from lib.dragonfree import launch
from lib import  settings




def window_exists(classname, windowname):
    try:
        win32ui.FindWindow(classname, windowname)
    except win32ui.error:
        return False
    else:
        return True





def press_digits(n):
    number = str(n)
    for digit in number:
        Key(digit)._execute()
        
def get_active_window_hwnd():
    return str(win32gui.GetForegroundWindow())

def get_active_window_title():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())

def get_active_window_path():
    name = win32gui.GetForegroundWindow()
    t, p = win32process.GetWindowThreadProcessId(name)
    handle = win32api.OpenProcess(0x0410, False, p)
    return win32process.GetModuleFileNameEx(handle, 0)

def get_window_by_title(title):
    hwnd = win32gui.FindWindowEx(0, 0, 0, title)
    return hwnd




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
    msg= list_to_string(sys.exc_info())
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


def py2exe_compile(choice):
    # the contents of this function have been replaced by instructions to do it manually
    #
    # copy generic dependencies: something_run.py, ["utilities.py", "paths.py", "settings.py"], ["compile.bat", "icon.ico", "msvcp90.dll", "msvcr90.dll"]
    # rename something_run.py to run.py
    # copy the python file
    # copy specific dependencies 
    # (dptools requires ["argparse.py", "_keyCodes.py", "_myclickLocations.py", "_mycommon.py"])
    # (element requires "tk85.dll", "tcl85.dll")
    # run the batch file compile.bat
    print "this function has been removed "

def reboot():
    launch.run('python C:/NatLink/NatLink/MacroSystem/lib/dragonfree/launch.py -r'.split())


