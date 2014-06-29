from dragonfly import *
import os,sys
import httplib
import paths, utilities
import helpdisplay

BASE_PATH = paths.get_base()
MMT_PATH = paths.get_mmt()

def suicide():
    BringApp(BASE_PATH + r"\suicide.bat")._execute()
    
def open_and(text,text2):
    print text
    print text2

def run_element():
    
    try:
        c = httplib.HTTPConnection('localhost', 8080)
        c.request('POST', '/process', '{}')
        doc = c.getresponse().read()
        print doc
    except Exception:
        for line in sys.exc_info():
            print line

class MainRule(MappingRule):
    global MMT_PATH
    mapping = {
    # Dragon NaturallySpeaking management
    'reboot dragon':                Function(utilities.clear_pyc)+Playback([(["stop", "listening"], 0.5), (["wake", 'up'], 0.0)]),
	'(lock Dragon | deactivate)':   Playback([(["go", "to", "sleep"], 0.0)]),
	'scratch':           			Playback([(["scratch", "that"], 0.0)]),
    '(number|numbers) mode':        Playback([(["numbers", "mode", "on"], 0.0)]),
    'spell mode':                   Playback([(["spell", "mode", "on"], 0.0)]),
    'dictation mode':               Playback([(["dictation", "mode", "on"], 0.0)]),
    'normal mode':                  Playback([(["normal", "mode", "on"], 0.0)]),
    "dragon (death | suicide) and rebirth":   Function( suicide ),
    
    # monitor management
    'toggle monitor one':           BringApp(MMT_PATH, r"/switch",r"\\.\DISPLAY1"),
    'toggle monitor two':           BringApp(MMT_PATH, r"/switch",r"\\.\DISPLAY2"),
    
    # window management
    "open <text> and <text2>":      Function(open_and, extra={'text','text2'}),
    "alt tab":                      Key( "w-backtick"),#activates Switcher
    'minimize':                     Playback([(["minimize", "window"], 0.0)]),
    'maximize':                     Playback([(["maximize", "window"], 0.0)]),
    
    "open natlink folder":          BringApp("explorer", "C:\NatLink\NatLink\MacroSystem"),
    
    "help <choice>":                Function(helpdisplay.get_help,extra={"choice"}),
    "variable":                     BringApp("python","variable.py"),
    "test feature":                 Function(run_element),
    }
    extras = [
              IntegerRef("n", 1, 1000),
              Dictation("text"),
              Dictation("text2"),
              Dictation("text3"),
              Choice("choice",
                    {"alphabet": "configalphabet.txt", "python": "configpython.txt", 
                    }),
             ]
    defaults ={"n": 1,
               "text": ""
               }

grammar = Grammar('Global')
grammar.add_rule(MainRule())
grammar.load()
