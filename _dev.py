from dragonfly import (Function, Key, BringApp, Text, WaitWindow, IntegerRef, Dictation, Repeat, Grammar, MappingRule)
from dragonfly.actions.action_focuswindow import FocusWindow

from asynch.mouse.legion import LegionScanner
from lib import utilities, settings
from lib.dragonfree import launch


def experiment(text):
    '''this function is for tests'''
    try:
        ''''''
        import natlink
        print natlink.getCurrentModule()
        
            
    except Exception:
        utilities.simple_log(False)

def rainbow():
    launch.run(["pythonw", settings.SETTINGS["paths"]["RAINBOW_PATH"], "-m", "r"])

def legion():
    ls = LegionScanner()
    ls.scan()
    tscan = ls.get_update()
    launch.run(["pythonw", settings.SETTINGS["paths"]["LEGION_PATH"], "-t", tscan[0]])

def douglas():
    launch.run(["pythonw", settings.SETTINGS["paths"]["DOUGLAS_PATH"], "-m", "d"])

class DevRule(MappingRule):
    
    mapping = {
    'refresh directory':            Function(utilities.clear_pyc),
    "(show | open) documentation":  BringApp(settings.SETTINGS["paths"]["DEFAULT_BROWSER_PATH"]) + WaitWindow(executable=settings.get_default_browser_executable()) + Key('c-t') + WaitWindow(title="New Tab") + Text('http://dragonfly.readthedocs.org/en/latest') + Key('enter'),

    "open natlink folder":          BringApp("explorer", settings.SETTINGS["paths"]["BASE_PATH"].replace("/", "\\")),
    "reserved word <text>":         Key("dquote,dquote,left") + Text("%(text)s") + Key("right, colon, tab/5:5") + Text("Text(\"%(text)s\"),"),
    "experiment <text>":            Function(experiment, extra="text"),
    
    "rainbow demo":                 Function(rainbow),
    "Legion demo":                  Function(legion),
    "Douglas demo":                 Function(douglas),
    
    
    }
    extras = [
              Dictation("text"),
              Dictation("textnv"),
              IntegerRef("n", 1, 100),
             ]
    defaults = {
               "text": ""
               }


grammar = None

def load():
    grammar = Grammar('development')
    grammar.add_rule(DevRule())
    grammar.load()

if settings.SETTINGS["miscellaneous"]["dev_commands"]:
    load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
