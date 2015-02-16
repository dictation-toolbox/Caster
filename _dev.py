from dragonfly import (Function, Key, BringApp, Text, WaitWindow, IntegerRef, Dictation, Choice, Grammar, MappingRule)
from dragonfly.actions.action_mimic import Mimic

from asynch.sikuli import sikuli
from lib import utilities, settings

# def dec1(f):
#     def new_f():
#         print "Entering", f.__name__
#         f()
#         print "Exited", f.__name__
#     return new_f
# from dec import dec1
# 
# @dec1
# def my_function():
#     print "k"
#     
# my_function()

def experiment():
    '''this function is for tests'''
    try: 
        ''''''
#         SelectiveAction(Text("eclipse"), ["eclipse.exe"])._execute()
    except Exception:
        utilities.simple_log(False)



class DevRule(MappingRule):
    
    mapping = {
    'refresh directory':            Function(utilities.clear_pyc),
    "(show | open) documentation":  BringApp(settings.SETTINGS["paths"]["DEFAULT_BROWSER_PATH"]) + WaitWindow(executable=settings.get_default_browser_executable()) + Key('c-t') + WaitWindow(title="New Tab") + Text('http://dragonfly.readthedocs.org/en/latest') + Key('enter'),

    "open natlink folder":          BringApp("explorer", settings.SETTINGS["paths"]["BASE_PATH"].replace("/", "\\")),
    "reserved word <text>":         Key("dquote,dquote,left") + Text("%(text)s") + Key("right, colon, tab/5:5") + Text("Text(\"%(text)s\"),"),
    "experiment":                   Function(experiment),
    
    
    }
    extras = [
              Dictation("text"),
              
             ]
    defaults = {
               "text": "", 
               }


grammar = None

def load():
    grammar=Grammar('development')
    grammar.add_rule(DevRule())
    grammar.load()

if settings.SETTINGS["miscellaneous"]["dev_commands"]:
    load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
