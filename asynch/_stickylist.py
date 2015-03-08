import time
import xmlrpclib

from dragonfly import (Function, Text, Grammar, Choice,
                       IntegerRef, Dictation, Mimic, MappingRule)

from lib import  settings, utilities
from lib import control
from lib.dragonfree import launch


def communicate():
    return xmlrpclib.ServerProxy("http://127.0.0.1:" + str(settings.S_LIST_LISTENING_PORT))

def kill():
    communicate().kill()

def add_symbol(sticky):
    Mimic("copy", "one")._execute()
    control.STICKY_LIST.append(control.MULTI_CLIPBOARD["1"])
    utilities.save_json_file(control.STICKY_LIST, settings.SETTINGS["paths"]["S_LIST_JSON_PATH"])
    if utilities.window_exists(None, settings.S_LIST_VERSION):
        communicate().add_symbol(control.MULTI_CLIPBOARD["1"])
    else:
        enable_sticky_list(sticky)

def get_symbol(n, sticky):
    n = int(n) - 1
    if n < 0 or n > len(control.STICKY_LIST) - 1:
        return
    Text(control.STICKY_LIST[n])._execute()
    if not utilities.window_exists(None, settings.S_LIST_VERSION):
        enable_sticky_list(sticky)

def remove_word(n, sticky):
    n = int(n)
    del control.STICKY_LIST[n - 1]
    utilities.save_json_file(control.STICKY_LIST, settings.SETTINGS["paths"]["S_LIST_JSON_PATH"])
    if utilities.window_exists(None, settings.S_LIST_VERSION):
        communicate().remove_symbol(n)
    else:
        enable_sticky_list(sticky)

def enable_sticky_list(sticky):
    if utilities.get_window_by_title(settings.S_LIST_VERSION) == 0 and sticky == 1:
        launch.run(["pythonw", settings.SETTINGS["paths"]["STICKY_LIST_PATH"]])
        time.sleep(2)

def do_enable():
    enable_sticky_list(1)

# pita examples on this file: "three key", "3G"
# SSticky copy threeky copy toage[<sticky>]gNatLinkNatLinkNatLinkNatLink
class SListUsageRule(MappingRule):
    mapping = {
    "L add [<sticky>]":             Function(add_symbol),
    "L get <n> [<sticky>]":         Function(get_symbol),
    "L remove <n> [<sticky>]":      Function(remove_word),
    
    "L run":                        Function(do_enable),
    "L kill":                       Function(kill),
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

control.STICKY_LIST = utilities.load_json_file(settings.SETTINGS["paths"]["S_LIST_JSON_PATH"])
r = SListUsageRule()
grammar = Grammar('SListUsageRule')
grammar.add_rule(r)
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
