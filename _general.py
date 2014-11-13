import sys, time

from dragonfly import (BringApp, Key, Function, Grammar, Playback,
                       IntegerRef, Dictation, Choice, WaitWindow, MappingRule, Text)

from lib import paths, utilities, settings, navigation, ccr, legion, password


ccr.refresh()
utilities.clean_temporary_files()

def fix_Dragon_double():
    try:
        lr = utilities.DICTATION_CACHE[len(utilities.DICTATION_CACHE)-1]
        lu = " ".join(lr)
        Key("left/5:" + str(len(lu)) + ", del")._execute()
    except Exception:
        utilities.report(utilities.list_to_string(sys.exc_info()))
    
def flip():
    Playback([(["alt", "tab"], 0.0)])._execute()
    WaitWindow(executable="Switcher.exe", timeout=5)._execute()
    if utilities.window_exists(None, settings.ELEMENT_VERSION):
        Playback([(["choose", "three"], 0.0)])._execute()
    else:
        Playback([(["choose", "two"], 0.0)])._execute()
        
def repeat_that(n):
    try:
        if len(utilities.DICTATION_CACHE)>0:
            for i in range(int(n)):
                Playback([([str(x) for x in " ".join(utilities.DICTATION_CACHE[len(utilities.DICTATION_CACHE)-1]).split()], 0.0)])._execute()
    except Exception:
        utilities.report(utilities.list_to_string(sys.exc_info()))

def switch_monitors():
    debug = False
    try:
        do_flip=settings.SETTINGS["last_monitor_was_flipped"]
        monitors=utilities.parse_monitor_scan(utilities.scan_monitors())
        
        if debug:
            print "active: "
            print monitors["active"]
            print "inactive: "
            print monitors["inactive"]
        #to do: stop hard coding it using the second monitor
        if len(monitors["active"]) == 1 and len(monitors["inactive"]) > 0:
            # preserve orientation information
            settings.SETTINGS["last_monitor_was_flipped"]=monitors["active"][0]["orientation"].startswith("180")
            settings.save_config()
            
            # activate the inactive monitor
            BringApp(paths.MMT_PATH, r"/switch", monitors["inactive"][0]["name"])._execute()
            time.sleep(2)
            
            # set the orientation
            if do_flip:
                BringApp(paths.MMT_PATH, r"/SetOrientation", monitors["inactive"][0]["name"], "180")._execute()
            else:
                BringApp(paths.MMT_PATH, r"/SetOrientation", monitors["inactive"][0]["name"], "0")._execute()
            time.sleep(5)
            
            # deactivate the active monitor
            BringApp(paths.MMT_PATH, r"/switch", monitors["active"][0]["name"])._execute()
            time.sleep(2)
            
            # set the resolution
            BringApp(paths.NIRCMD_PATH, "setdisplay", str(monitors["inactive"][0]["resolution"][0]), str(monitors["inactive"][0]["resolution"][1]), "32")._execute()
#             time.sleep(10)
            

        # other cases go here
    except Exception:
        utilities.report(utilities.list_to_string(sys.exc_info()))
        #
    
class MainRule(MappingRule):
    
    @staticmethod
    def generate_CCR_choices():
        choices = {}
#         utilities.remote_debug()
        for ccr_choice in utilities.get_list_of_ccr_config_files():
            choices[ccr_choice] = ccr_choice
        return Choice("ccr_mode", choices)
    
    mapping = {
    # Dragon NaturallySpeaking management
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
    "remax":                        Key("a-space/10,r/10,a-space/10,x"), 
    
    # development related
    "open natlink folder":          BringApp("explorer", "C:\NatLink\NatLink\MacroSystem"),
    "reserved word <text>":         Key("dquote,dquote,left") + Text("%(text)s") + Key("right, colon, tab/5:5") + Text("Text(\"%(text)s\"),"),
    "test Legion":                  Function(legion.get_screen_signature),
    
    # passwords
    'hash password <text> <text2> <text3>':                    Function(password.hash_password, extra={'text', 'text2', 'text3'}),
    'get password <text> <text2> <text3>':                     Function(password.get_password, extra={'text', 'text2', 'text3'}),
    'get restricted password <text> <text2> <text3>':          Function(password.get_restricted_password, extra={'text', 'text2', 'text3'}),
    'quick pass <text> <text2> <text3>':                       Function(password.get_simple_password, extra={'text', 'text2', 'text3'}),
    
    # miscellaneous
    "<enable_disable> <ccr_mode>":  Function(ccr.change_CCR, extra={"enable_disable", "ccr_mode"}),
    "again <n> [times]":      Function(repeat_that, extra={"n"}),
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

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
    ccr.unload()
