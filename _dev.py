from dragonfly import (Function, Key, BringApp, Text, WaitWindow, IntegerRef, Dictation, Repeat, Grammar, MappingRule)

from lib import utilities, settings


def experiment(text):
    '''this function is for tests'''
    try:
        ''''''
        
    except Exception:
        utilities.simple_log(False)

def printD(p, nn):
    print p, nn

class DevRule(MappingRule):
    
    mapping = {
    'refresh directory':            Function(utilities.clear_pyc),
    "(show | open) documentation":  BringApp(settings.SETTINGS["paths"]["DEFAULT_BROWSER_PATH"]) + WaitWindow(executable=settings.get_default_browser_executable()) + Key('c-t') + WaitWindow(title="New Tab") + Text('http://dragonfly.readthedocs.org/en/latest') + Key('enter'),

    "open natlink folder":          BringApp("explorer", settings.SETTINGS["paths"]["BASE_PATH"].replace("/", "\\")),
    "reserved word <text>":         Key("dquote,dquote,left") + Text("%(text)s") + Key("right, colon, tab/5:5") + Text("Text(\"%(text)s\"),"),
    "experiment <text>":            Function(experiment, extra="text"),
    "printing _test <n>":            Function(printD, nn=12, p=1)* Repeat(extra="n"), 
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
