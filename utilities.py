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
        
def get_active_window():
    name = win32gui.GetForegroundWindow()
    t,p = win32process.GetWindowThreadProcessId(name)
    handle = win32api.OpenProcess(0x0410,False,p)
    print win32process.GetModuleFileNameEx( handle, 0 )