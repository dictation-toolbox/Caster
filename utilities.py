'''
Created on Jun 12, 2014

@author: dave
'''
from dragonfly import Key
import win32gui, win32process, win32api

def press_digits(n):
    number=str(n)
    for digit in number:
        Key(digit).execute()
        
def get_active_window_hwnd():
    return str(win32gui.GetForegroundWindow())

def get_active_window_path():
    name = win32gui.GetForegroundWindow()
    t,p = win32process.GetWindowThreadProcessId(name)
    handle = win32api.OpenProcess(0x0410,False,p)
    return win32process.GetModuleFileNameEx( handle, 0 )