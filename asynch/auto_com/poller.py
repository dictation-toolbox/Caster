import sys
import time

import win32api
import win32con


try:
    # this file may be executed externally to Dragon
    BASE_PATH = "C:/NatLink/NatLink/MacroSystem"
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
finally:
    from lib import  settings, utilities

print "Caster Auto-Command Mode External Window Checker"

last = 0

while True:
    current = utilities.get_active_window_hwnd()
    if last != current:
        last = current
        win32api.keybd_event(int(settings.SETTINGS["auto_com"]["pyHook_KeyID"]), 0, 0, 0)
        time.sleep(.05)
        win32api.keybd_event(int(settings.SETTINGS["auto_com"]["pyHook_KeyID"]), 0 , win32con.KEYEVENTF_KEYUP , 0)
        print "window hwnd: ", current
      
    time.sleep(settings.SETTINGS["auto_com"]["interval"])
