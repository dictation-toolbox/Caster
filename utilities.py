'''
Created on Jun 12, 2014

@author: dave
'''
from dragonfly import Key
import win32gui, win32process, win32api
import os
import paths

BASE_PATH = paths.get_base()

def press_digits(n):
    number=str(n)
    for digit in number:
        Key(digit).execute()
        
def get_active_window_hwnd():
    return str(win32gui.GetForegroundWindow())

def get_active_window_title():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())

def get_active_window_path():
    name = win32gui.GetForegroundWindow()
    t,p = win32process.GetWindowThreadProcessId(name)
    handle = win32api.OpenProcess(0x0410,False,p)
    return win32process.GetModuleFileNameEx( handle, 0 )

def clear_pyc():
    global BASE_PATH
    os.chdir(BASE_PATH)
    for files in os.listdir("."):
        if files.endswith(".pyc"):
            filepath=BASE_PATH+files
            os.remove(filepath)
            print "Deleted: "+filepath