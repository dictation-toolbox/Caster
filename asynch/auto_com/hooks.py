from dragonfly import Mimic

from lib import control, utilities, settings
from lib.dragonfree import launch

_LAST = False
_RUN_FIRST_TIME = False
_NL=None
_ON=Mimic("command", "mode", "on")
_OFF=Mimic("command", "mode", "off")
first=[]

if control.DEP.PYHOOK:
    import pyHook
if control.DEP.PYHOOK:
    import natlink

def OnKeyboardEvent(event):
    print 133
    try:
        global _LAST, _RUN_FIRST_TIME, _ON, _OFF
        changed = False
        if not _RUN_FIRST_TIME:
            changed = True
            _RUN_FIRST_TIME = True
        
        current_window=utilities.get_active_window_path(natlink).split("\\")[-1]
        print event.KeyID, current_window
        if int(event.KeyID) == int(settings.SETTINGS["auto_com"]["pyHook_KeyID"]):
            if current_window in settings.SETTINGS["auto_com"]["executables"]:
#             if utilities.get_active_window_path(_NL).split("\\")[-1] in settings.SETTINGS["auto_com"]["executables"]:
                if _LAST == False:
                    changed = True
                _LAST = True
            else:
                if _LAST == True:
                    changed = True
                _LAST = False
                 
        # return True to pass the event to other handlers
        if changed:
            print "change detected"
            if _LAST:
                _ON.execute()
            else:
                _OFF.execute()
    except Exception:
        utilities.simple_log(False)
    
    refresh_hooks()
    return True

def initialize_auto_com_external():
    refresh_hooks()
    launch.run(["python", "C:/NatLink/NatLink/MacroSystem/asynch/auto_com/poller.py"])

def refresh_hooks():
    if control.HOOK_MANAGER!=None:
        control.HOOK_MANAGER.KeyDown=None
        control.HOOK_MANAGER.UnhookKeyboard()
        control.HOOK_MANAGER=None
        
    control.HOOK_MANAGER = pyHook.HookManager()
    control.HOOK_MANAGER.KeyDown = OnKeyboardEvent
    control.HOOK_MANAGER.HookKeyboard()
    
