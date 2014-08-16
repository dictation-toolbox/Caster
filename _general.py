from dragonfly import (BringApp, Key, Function, Grammar, Playback, 
                       IntegerRef,Dictation,Choice,WaitWindow,MappingRule)
from lib import paths, utilities, settings, navigation,ccr
import os


BASE_PATH = paths.get_base()
MMT_PATH = paths.get_mmt()
monitor_orientation=0
ccr.refresh()

def flip():
    Playback([(["alt", "tab"], 0.0)])._execute()
    WaitWindow(executable="Switcher.exe")._execute()
    if utilities.window_exists(None, settings.ELEMENT_VERSION):
        Playback([(["choose", "three"], 0.0)])._execute()
    else:
        Playback([(["choose", "two"], 0.0)])._execute()

def flip_monitor_orientations():
    global monitor_orientation
    if monitor_orientation==0:
        monitor_orientation= 180
    else:
        monitor_orientation=0
    BringApp(paths.get_mmt(),r"/SetOrientation",r"\\.\DISPLAY1",str(monitor_orientation),r"\\.\DISPLAY2",str(monitor_orientation))._execute()#

    
class MainRule(MappingRule):
    global MMT_PATH
    
    @staticmethod
    def generate_CCR_choices():
        choices={}
        for f in os.listdir(paths.get_generic_config_path()):
            if f.endswith(".txt"):
                ccr_choice = f.replace("config","").replace(".txt","")
                choices[ccr_choice]=ccr_choice
        return Choice("ccr_mode", choices)
    
    mapping = {
    # Dragon NaturallySpeaking management
    'reboot dragon':                Function(utilities.clear_pyc)+Playback([(["stop", "listening"], 0.5), (["wake", 'up'], 0.0)]),
	'(lock Dragon | deactivate)':   Playback([(["go", "to", "sleep"], 0.0)]),
    '(number|numbers) mode':        Playback([(["numbers", "mode", "on"], 0.0)]),
    'spell mode':                   Playback([(["spell", "mode", "on"], 0.0)]),
    'dictation mode':               Playback([(["dictation", "mode", "on"], 0.0)]),
    'normal mode':                  Playback([(["normal", "mode", "on"], 0.0)]),
    "dragon death and rebirth":     BringApp(BASE_PATH + r"\suicide.bat"),
    
    # hardware management
    'toggle monitor one':           BringApp(MMT_PATH, r"/switch",r"\\.\DISPLAY1"),
    'toggle monitor two':           BringApp(MMT_PATH, r"/switch",r"\\.\DISPLAY2"),
    "monitors one eighty":          Function(flip_monitor_orientations),
    "(<volume_mode> [system] volume [to] <nnv> | volume <volume_mode> <nnv>)": Function(navigation.volume_control, extra={'nnv','volume_mode'}),
    
    # window management
    "alt tab":                      Key("w-backtick"),#activates Switcher
    "flip":                         Function(flip),
    'minimize':                     Playback([(["minimize", "window"], 0.0)]),
    'maximize':                     Playback([(["maximize", "window"], 0.0)]),
    
    # development related
    "set alarm [<minutes> minutes]":Function(utilities.alarm, extra={"minutes"}),
    "open natlink folder":          BringApp("explorer", "C:\NatLink\NatLink\MacroSystem"),
    "compile <choice>":             Function(utilities.py2exe_compile, extra={"choice"}),
    
    # miscellaneous
    "<enable_disable> <ccr_mode>":  Function(ccr.change_CCR, extra={"enable_disable", "ccr_mode"}),
    }
    extras = [
              IntegerRef("n", 1, 1000),
              IntegerRef("nnv", 1, 100),
              IntegerRef("minutes", 1, 720),
              Dictation("text"),
              Dictation("text2"),
              Dictation("text3"),
              Choice("choice",
                    {"alarm": "alarm", "custom grid": "CustomGrid", "element": "element"
                    }),
              Choice("enable_disable",
                    {"enable": "enable", "disable": "disable"
                    }),
              Choice("volume_mode",
                    {"set": "set", "increase": "up", "decrease": "down",
                     "up":"up","down":"down"
                     }),
              generate_CCR_choices.__func__()
             ]
    defaults ={"n": 1, "minutes": 20, "nnv": 1,
               "text": "", "volume_mode": "setsysvolume"
               }


grammar = Grammar('general')
grammar.add_rule(MainRule())
grammar.load()


def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
    ccr.unload()