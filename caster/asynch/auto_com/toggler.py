from dragonfly import Mimic

from caster.asynch.auto_com import language
from caster.lib import control, utilities, settings
from caster.lib.dfplus.state.short import R


_LAST = False
_HAS_RUN_FIRST_TIME = False

_ON = R(Mimic("command", "mode", "on"), rdescript="Command Mode On")
_OFF = R(Mimic("command", "mode", "off"), rdescript="Command Mode Off")

if control.nexus().dep.NATLINK:
    import natlink

def toggle():
    if natlink.getMicState()!="on":
        return
    
    '''determines whether to toggle and then if so toggles appropriately'''
    global _LAST, _HAS_RUN_FIRST_TIME, _ON, _OFF
    should_toggle = False
    if not _HAS_RUN_FIRST_TIME:
        should_toggle = True
        _HAS_RUN_FIRST_TIME = True
    
    if not settings.SETTINGS["auto_com"]["change_language_only"]:
        current_window = utilities.get_active_window_path(natlink).split("\\")[-1]
        should_be_on = current_window in settings.SETTINGS["auto_com"]["executables"]
        should_toggle = should_be_on != _LAST
        _LAST = should_be_on
        
        if should_toggle:
            e = _ON if _LAST else _OFF
            e.execute()
            
    
    # language switching section
    if settings.SETTINGS["auto_com"]["change_language"]:
        language.toggle_language()

def initialize_auto_com_internal():
    control.nexus().timer.add_callback(toggle, settings.SETTINGS["auto_com"]["interval"])
    
