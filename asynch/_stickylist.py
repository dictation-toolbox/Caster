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

def add_symbol():
    Mimic("copy", "one")._execute()
    communicate().add_symbol(control.MULTI_CLIPBOARD["1"])
    control.STICKY_LIST.append(control.MULTI_CLIPBOARD["1"])
    utilities.save_json_file(control.STICKY_LIST, settings.SETTINGS["paths"]["S_LIST_JSON_PATH"])

def get_symbol(n):
    n = int(n)
    Text(communicate().get_symbol(n))._execute()

def remove_word(n):
    n = int(n)
    communicate().remove_symbol(n)
    del control.STICKY_LIST[n - 1]
    utilities.save_json_file(control.STICKY_LIST, settings.SETTINGS["paths"]["S_LIST_JSON_PATH"])

def enable_sticky_list(sticky):
    if utilities.get_window_by_title(settings.S_LIST_VERSION) == 0 and sticky == 1:
        control.STICKY_LIST = utilities.load_json_file(settings.SETTINGS["paths"]["S_LIST_JSON_PATH"])
        launch.run(["pythonw", settings.SETTINGS["paths"]["STICKY_LIST_PATH"]])
        time.sleep(1)
# pita examples on this file: "three key", "3G"
# SSticky copy threeky copy toage
class SListUsageRule(MappingRule):
    mapping = {
    "L add [<sticky>]":             Function(enable_sticky_list) + Function(add_symbol),
    "L get <n> [<sticky>]":         Function(enable_sticky_list) + Function(get_symbol),
    "L remove <n> [<sticky>]":      Function(enable_sticky_list) + Function(remove_word),
    
    "L run":                        Function(enable_sticky_list, sticky=1),
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

r = SListUsageRule()
grammar = Grammar('SListUsageRule')
grammar.add_rule(r)
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
