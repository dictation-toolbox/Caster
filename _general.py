import natlink
from natlinkutils import GrammarBase
import os
import sys, codecs, time

from dragonfly import (BringApp, Key, Function, Grammar, Playback,
                       IntegerRef, Dictation, Choice, WaitWindow, MappingRule, Text)

from lib import paths, utilities, settings, navigation, ccr, legion


ccr.refresh()
utilities.clean_temporary_files()

def fix_Dragon_double():
    try:
        lr = utilities.LAST_RESULT
        lu = " ".join(lr)
        Key("left/5:" + str(len(lu)) + ", del")._execute()
    except Exception:
        utilities.report(utilities.list_to_string(sys.exc_info()))
    
def flip():
    Playback([(["alt", "tab"], 0.0)])._execute()
    WaitWindow(executable="Switcher.exe")._execute()
    if utilities.window_exists(None, settings.ELEMENT_VERSION):
        Playback([(["choose", "three"], 0.0)])._execute()
    else:
        Playback([(["choose", "two"], 0.0)])._execute()

def switch_monitors():
    debug = True
    try:
        if not os.path.exists(paths.MONITOR_INFO_PATH):
            os.makedirs(paths.MONITOR_INFO_PATH)
        monitor_scan_path = paths.MONITOR_INFO_PATH + utilities.current_time_to_string() + ".txt"
        BringApp(paths.MMT_PATH, r"/stext", monitor_scan_path)._execute()
        time.sleep(1)
        content = None
        with codecs.open(monitor_scan_path, "r", encoding="utf-16") as f:
            content = f.readlines()
        is_active = False
        active_monitors = []
        inactive_monitors = []
        resolution = None
        # Maximum Resolution: 1600 X 900
        for line in content:
            line = line.replace(" ", "")
            if line.startswith("Maximum"):
                line = line.split(":")[1]
                rwh = line = line.split("X")
                resolution = (int(rwh[0]), int(rwh[1]))
            elif line.startswith("Active"):
                line = line.split(":")[1]
                is_active = line.startswith("Yes")
            elif line.startswith("Name"):
                line = line.split(":")[1]
                if is_active:
                    active_monitors.append(line.replace("\r\n", ""))
                else:
                    inactive_monitors.append((line.replace("\r\n", ""), resolution))
        if debug:
            print "active: "
            print active_monitors
            print "inactive: "
            print inactive_monitors
        how_many_active = len(active_monitors)
        how_many_inactive = len(inactive_monitors)
        if how_many_active == 1 and how_many_inactive > 0:
            BringApp(paths.MMT_PATH, r"/switch", inactive_monitors[0][0])._execute()
            time.sleep(2)
            BringApp(paths.MMT_PATH, r"/switch", active_monitors[0])._execute()
            time.sleep(2)
            BringApp(paths.NIRCMD_PATH, "setdisplay", str(inactive_monitors[0][1][0]), str(inactive_monitors[0][1][1]), "32")._execute()
        # other cases go here
    except Exception:
        utilities.report(utilities.list_to_string(sys.exc_info()))
            
    
class MainRule(MappingRule):
    
    @staticmethod
    def generate_CCR_choices():
        choices = {}
        for ccr_choice in utilities.get_list_of_individual_config_files():
            choices[ccr_choice] = ccr_choice
        return Choice("ccr_mode", choices)
    
    mapping = {
    # Dragon NaturallySpeaking management
    "test Legion":                  Function(legion.get_screen_signature),
    'refresh directory':            Function(utilities.clear_pyc),
	'(lock Dragon | deactivate)':   Playback([(["go", "to", "sleep"], 0.0)]),
    '(number|numbers) mode':        Playback([(["numbers", "mode", "on"], 0.0)]),
    'spell mode':                   Playback([(["spell", "mode", "on"], 0.0)]),
    'dictation mode':               Playback([(["dictation", "mode", "on"], 0.0)]),
    'normal mode':                  Playback([(["normal", "mode", "on"], 0.0)]),
    "reboot dragon":                BringApp(paths.BASE_PATH + r"\bin\suicide.bat"),
    "fix dragon double":            Function(fix_Dragon_double),
    "(show | open) documentation":  BringApp('C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe') + WaitWindow(executable="chrome.exe") + Key('c-t') + WaitWindow(title="New Tab") + Text('http://dragonfly.readthedocs.org/en/latest') + Key('enter'),
    # http://dragonfly.readthedocs.org/en/latest
    
    # hardware management
    "(switch | change) monitors":              Function(switch_monitors),
    "(<volume_mode> [system] volume [to] <nnv> | volume <volume_mode> <nnv>)": Function(navigation.volume_control, extra={'nnv', 'volume_mode'}),
    
    # window management
    "alt tab":                      Key("w-backtick"),  # activates Switcher
    "flip":                         Function(flip),
    'minimize':                     Playback([(["minimize", "window"], 0.0)]),
    'maximize':                     Playback([(["maximize", "window"], 0.0)]),
    
    # development related
    "open natlink folder":          BringApp("explorer", "C:\NatLink\NatLink\MacroSystem"),
    "compile <choice>":             Function(utilities.py2exe_compile, extra={"choice"}),
    "reserved word <text>":         Key("dquote,dquote,left") + Text("%(text)s") + Key("right, colon, tab/5:5") + Text("Text(\"%(text)s\"),"),
    
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
                     "up":"up", "down":"down"
                     }),
              generate_CCR_choices.__func__()
             ]
    defaults = {"n": 1, "minutes": 20, "nnv": 1,
               "text": "", "volume_mode": "setsysvolume"
               }


grammar = Grammar('general')
grammar.add_rule(MainRule())
grammar.load()

# modeled on Joel Gould's "repeat that" grammar.
class SaveLastGrammar(GrammarBase):

    gramSpec = """
        <start> exported = {emptyList};
    """

    def initialize(self):
        self.load(self.gramSpec, allResults=1)
        self.activateAll()

    def gotResultsObject(self, recogType, resObj):
        
        if recogType == 'reject':
            utilities.LAST_RESULT = None
        elif resObj.getWords(0)[:1] != ['repeat', 'that']:
            utilities.LAST_RESULT = resObj.getWords(0)
            
class AgainGrammar(GrammarBase):

    gramSpec = """
        <start> exported = repeat that
          [ ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
              10 | 20 | 30 | 40 | 50 | 100 ) times ];
    """
    
    def initialize(self):
        self.load(self.gramSpec)
        self.activateAll()

    def gotResults_start(self, words, fullResults):
        
        if len(words) > 2:
            count = int(words[2])
        else:
            count = 1
        if utilities.LAST_RESULT:
            for i in range(count):
                natlink.recognitionMimic(utilities.LAST_RESULT)

slGrammar = SaveLastGrammar()
slGrammar.initialize()
rGrammar = AgainGrammar()
rGrammar.initialize()

def unload():
    global slGrammar
    global rGrammar
    if slGrammar:
        slGrammar.unload()
    slGrammar = None
    if rGrammar:
        rGrammar.unload()
    rGrammar = None

    global grammar
    if grammar: grammar.unload()
    grammar = None
    ccr.unload()
