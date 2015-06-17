from subprocess import Popen
import time

from dragonfly import (Function, Text, Grammar, Choice,
                       IntegerRef, Dictation, Mimic, MappingRule)

from caster.lib import  settings, utilities, navigation
from caster.lib import control
from caster.lib.dfplus.state.short import R


def kill():
    control.nexus().comm.get_com("sticky_list").kill()

def add_symbol(sticky):
    sticky_key="sticky_key"
    navigation.clipboard_to_file(sticky_key, True)
    time.sleep(0.1)
    control.nexus().sticky.append(control.nexus().clip[sticky_key])
    utilities.save_json_file(control.nexus().sticky, settings.SETTINGS["paths"]["S_LIST_JSON_PATH"])
    if utilities.window_exists(None, settings.S_LIST_VERSION):
        control.nexus().comm.get_com("sticky_list").add_symbol(control.nexus().clip[sticky_key])
    else:
        enable_sticky_list(sticky)

def get_symbol(n, sticky):
    n = int(n) - 1
    if n < 0 or n > len(control.nexus().sticky) - 1:
        return
    Text(control.nexus().sticky[n])._execute()
    if not utilities.window_exists(None, settings.S_LIST_VERSION):
        enable_sticky_list(sticky)

def remove_word(n, sticky):
    n = int(n)
    del control.nexus().sticky[n - 1]
    utilities.save_json_file(control.nexus().sticky, settings.SETTINGS["paths"]["S_LIST_JSON_PATH"])
    if utilities.window_exists(None, settings.S_LIST_VERSION):
        control.nexus().comm.get_com("sticky_list").remove_symbol(n)
    else:
        enable_sticky_list(sticky)

def clear():
    control.nexus().sticky=[]
    utilities.save_json_file(control.nexus().sticky, settings.SETTINGS["paths"]["S_LIST_JSON_PATH"])
    if utilities.window_exists(None, settings.S_LIST_VERSION):
        control.nexus().comm.get_com("sticky_list").clear()

def enable_sticky_list(sticky):
    if utilities.get_window_by_title(settings.S_LIST_VERSION) == 0 and sticky == 1:
        Popen(["pythonw", settings.SETTINGS["paths"]["STICKY_LIST_PATH"]])
        time.sleep(2)

def do_enable():
    enable_sticky_list(1)

class SListUsageRule(MappingRule):
    mapping = {
    "L add [<sticky>]":             R(Function(add_symbol), rdescript="Add Selected To Sticky List"),
    "L get <n> [<sticky>]":         R(Function(get_symbol), rdescript="Retrieve From Sticky List"),
    "L remove <n> [<sticky>]":      R(Function(remove_word), rdescript="Remove From Sticky List"),
    "L clear":                      Function(clear),
    
    "L run":                        R(Function(do_enable), rdescript="Run Sticky List"),
    "L kill":                       R(Function(kill), rdescript="Shutdown Sticky List"),
    }   
    extras = [
              IntegerRef("n", 1, 200),
              Dictation("text"),
              Choice("sticky", {"run": 1}),
             ]
    defaults = {"n": 1,
               "text": "",
               "sticky": 0
               }

control.nexus().sticky = utilities.load_json_file(settings.SETTINGS["paths"]["S_LIST_JSON_PATH"])
r = SListUsageRule()
grammar = Grammar('SListUsageRule')
grammar.add_rule(r)
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
