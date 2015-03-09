from dragonfly import Mimic

from lib import control, utilities, settings
from lib.dragonfree import launch

_LAST = False
_HAS_RUN_FIRST_TIME = False

_ON = Mimic("command", "mode", "on")
_OFF = Mimic("command", "mode", "off")

if control.DEP.PYHOOK:
    import pyHook
if control.DEP.NATLINK:
    import natlink

def toggle():
    '''determines whether to toggle and then if so toggles appropriately'''
    global _LAST, _HAS_RUN_FIRST_TIME, _ON, _OFF
    should_toggle = False
    if not _HAS_RUN_FIRST_TIME:
        should_toggle = True
        _HAS_RUN_FIRST_TIME = True
    
    current_window = utilities.get_active_window_path(natlink).split("\\")[-1]
    should_be_on = current_window in settings.SETTINGS["auto_com"]["executables"]
    should_toggle = should_be_on != _LAST
    _LAST = should_be_on
    
    if should_toggle:
        e = _ON if _LAST else _OFF
        e.execute()

def on_keyboard_event(event):
    if int(event.KeyID) == int(settings.SETTINGS["auto_com"]["pyHook_KeyID"]):
        toggle()
    refresh_hooks()
    # return True to pass the event to other handlers
    return True

def initialize_auto_com_internal():
    control.TIMER_MANAGER.add_callback(toggle, settings.SETTINGS["auto_com"]["interval"])

def initialize_auto_com_external():
    refresh_hooks()
    launch.run(["python", "C:/NatLink/NatLink/MacroSystem/asynch/auto_com/poller.py"])

def refresh_hooks():
    if control.HOOK_MANAGER != None:
        control.HOOK_MANAGER.KeyDown = None
        control.HOOK_MANAGER.UnhookKeyboard()
        control.HOOK_MANAGER = None
        
    control.HOOK_MANAGER = pyHook.HookManager()
    control.HOOK_MANAGER.KeyDown = on_keyboard_event
    control.HOOK_MANAGER.HookKeyboard()
    
