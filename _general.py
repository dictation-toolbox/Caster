from dragonfly import (BringApp, Key, Function, Text, Grammar, Playback, 
                       IntegerRef,Dictation,Choice,WaitWindow,MappingRule)
import sys, httplib, json
import paths, utilities, helpdisplay

 

BASE_PATH = paths.get_base()
MMT_PATH = paths.get_mmt()

def suicide():
    BringApp(BASE_PATH + r"\suicide.bat")._execute()
    
def run_element():
    
    try:
        c = httplib.HTTPConnection('localhost', 8080)
        data_to_send={}
        data_to_send["test case"]="hello test case"
        c.request('POST', '/process', json.dumps(data_to_send))
        doc = c.getresponse().read()
        utilities.report(doc)
    except Exception:
        utilities.report(utilities.list_to_string(sys.exc_info()))

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
    "alt tab":                      Key( "w-backtick"),#activates Switcher
    "flip":                         Playback([(["alt", "tab"], 0.0)])+ WaitWindow(executable="Switcher.exe")+Playback([(["choose", "two"], 0.0)]),
    'minimize':                     Playback([(["minimize", "window"], 0.0)]),
    'maximize':                     Playback([(["maximize", "window"], 0.0)]),
    
    # miscellaneous
    "open natlink folder":          BringApp("explorer", "C:\NatLink\NatLink\MacroSystem"),
    "help <choice>":                Function(helpdisplay.get_help,extra={"choice"}),
    "element request":              Function(run_element),
    
    
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
