from dragonfly import (BringApp, Key, Function, Grammar, Playback, 
                       IntegerRef,Dictation,Choice,WaitWindow,MappingRule)
import paths, utilities

BASE_PATH = paths.get_base()
MMT_PATH = paths.get_mmt()
monitor_orientation=0

def flip_monitor_orientations():
    global monitor_orientation
    if monitor_orientation==0:
        monitor_orientation= 180
    else:
        monitor_orientation=0
    BringApp(paths.get_mmt(),r"/SetOrientation",r"\\.\DISPLAY1",str(monitor_orientation),r"\\.\DISPLAY2",str(monitor_orientation))._execute()#

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
    "dragon death and rebirth":     BringApp(BASE_PATH + r"\suicide.bat"),
    
    # monitor management
    'toggle monitor one':           BringApp(MMT_PATH, r"/switch",r"\\.\DISPLAY1"),
    'toggle monitor two':           BringApp(MMT_PATH, r"/switch",r"\\.\DISPLAY2"),
    "monitors one eighty":          Function(flip_monitor_orientations),
    
    # window management
    "alt tab":                      Key("w-backtick"),#activates Switcher
    "flip":                         Playback([(["alt", "tab"], 0.0)])+ WaitWindow(executable="Switcher.exe")+Playback([(["choose", "two"], 0.0)]),
    'minimize':                     Playback([(["minimize", "window"], 0.0)]),
    'maximize':                     Playback([(["maximize", "window"], 0.0)]),
    
    # development related
    "set alarm [<minutes> minutes]":Function(utilities.alarm, extra={"minutes"}),
    "open natlink folder":          BringApp("explorer", "C:\NatLink\NatLink\MacroSystem"),
    "compile <choice>":             Function(utilities.py2exe_compile, extra={"choice"}),
    
    # miscellaneous
    
    }
    extras = [
              IntegerRef("n", 1, 1000),
              IntegerRef("minutes", 1, 720),
              Dictation("text"),
              Dictation("text2"),
              Dictation("text3"),
              Choice("choice",
                    {"alarm": "alarm", "custom grid": "CustomGrid", "element": "element"
                    }),
             ]
    defaults ={"n": 1, "minutes": 20,
               "text": ""
               }

grammar = Grammar('Global')
grammar.add_rule(MainRule())
grammar.load()
