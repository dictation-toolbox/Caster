
from subprocess import Popen

from dragonfly import (Grammar, Playback, MappingRule, Key,
                       Dictation, IntegerRef, Function)

from caster.lib import settings, control, utilities
from caster.lib.dfplus.state.short import R

def launch_status():
    if not utilities.window_exists(None, settings.STATUS_WINDOW_TITLE):
        Popen(["pythonw", settings.SETTINGS["paths"]["STATUS_WINDOW_PATH"]])

def toggle_status():
    enabled = settings.SETTINGS["miscellaneous"]["status_window_enabled"]
    if enabled:
        control.nexus().intermediary.kill()
    else:
        launch_status()
    settings.SETTINGS["miscellaneous"]["status_window_enabled"] = not enabled
    settings.save_config()

def settings_window():
    Popen(["pythonw", settings.SETTINGS["paths"]["SETTINGS_WINDOW_PATH"]])

class CommandRule(MappingRule):

    mapping = {
        "toggle status window":     R(Function(toggle_status), rdescript="Toggle Status Window"), 
        "launch settings window":   R(Function(settings_window), rdescript="Launch Settings Window"), 
        }
    extras = []
    defaults = {}

#---------------------------------------------------------------------------

grammar = None

grammar = Grammar("Caster Windows")
grammar.add_rule(CommandRule())
grammar.load()

if settings.SETTINGS["miscellaneous"]["status_window_enabled"]:
    launch_status()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None