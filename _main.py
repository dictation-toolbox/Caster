
from dragonfly import (BringApp, Key, Function, Grammar, Playback, FocusWindow,
                       IntegerRef, Dictation, Choice, WaitWindow, MappingRule, Text)

from asynch.hmc import vocabulary_processing
from lib import control, settings, navigation, ccr, password, context
from lib import utilities


def experiment():
    '''this function is for testing things in development'''
    try: 
        context.get_macro_spec()
    except Exception:
        utilities.simple_log(False)

def fix_Dragon_double():
    try:
        lr = control.DICTATION_CACHE[len(control.DICTATION_CACHE)-1]
        lu = " ".join(lr)
        Key("left/5:" + str(len(lu)) + ", del")._execute()
    except Exception:
        utilities.simple_log(False)
        
def repeat_that(n):
    try:
        if len(control.DICTATION_CACHE)>0:
            for i in range(int(n)):
                Playback([([str(x) for x in " ".join(control.DICTATION_CACHE[len(control.DICTATION_CACHE)-1]).split()], 0.0)])._execute()
    except Exception:
        utilities.simple_log(False)

   
class MainRule(MappingRule):
    
    @staticmethod
    def generate_CCR_choices():
        choices = {}
        for ccr_choice in settings.get_list_of_ccr_config_files():
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
    "reboot dragon":                Function(utilities.reboot),
    "fix dragon double":            Function(fix_Dragon_double),
    "(show | open) documentation":  BringApp('C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe') + WaitWindow(executable="chrome.exe") + Key('c-t') + WaitWindow(title="New Tab") + Text('http://dragonfly.readthedocs.org/en/latest') + Key('enter'),
    "add word to vocabulary":       Function(vocabulary_processing.add_vocab),
    "delete word from vocabulary":  Function(vocabulary_processing.del_vocab),
    
    # hardware management
#     "(switch | change) monitors":              Function(switch_monitors),
    "(<volume_mode> [system] volume [to] <n> | volume <volume_mode> <n>)": Function(navigation.volume_control, extra={'n', 'volume_mode'}),
    
    # window management
    'minimize':                     Playback([(["minimize", "window"], 0.0)]),
    'maximize':                     Playback([(["maximize", "window"], 0.0)]),
    "remax":                        Key("a-space/10,r/10,a-space/10,x"), 
    
    # development related
    "open natlink folder":          BringApp("explorer", "C:\NatLink\NatLink\MacroSystem"),
    "reserved word <text>":         Key("dquote,dquote,left") + Text("%(text)s") + Key("right, colon, tab/5:5") + Text("Text(\"%(text)s\"),"),
    "experiment":                   Function(experiment),
    
    # passwords
    'hash password <text> <text2> <text3>':                    Function(password.hash_password, extra={'text', 'text2', 'text3'}),
    'get password <text> <text2> <text3>':                     Function(password.get_password, extra={'text', 'text2', 'text3'}),
    'get restricted password <text> <text2> <text3>':          Function(password.get_restricted_password, extra={'text', 'text2', 'text3'}),
    'quick pass <text> <text2> <text3>':                       Function(password.get_simple_password, extra={'text', 'text2', 'text3'}),
    
    # mouse alternatives
    "legion":                       Function(navigation.mouse_alternates, mode="legion"),
    "rainbow":                      Function(navigation.mouse_alternates, mode="rainbow"),
    "douglas":                      Function(navigation.mouse_alternates, mode="douglas"),
    
    # miscellaneous
    "<enable_disable> <ccr_mode>":  Function(ccr.change_CCR, extra={"enable_disable", "ccr_mode"}),
    "again <n> [times]":            Function(repeat_that, extra={"n"}),
    "begin recording macro":        Function(context.null_func),
    "end recording macro":          Function(context.get_macro_spec),
    "delete recorded macros":       Function(context.delete_recorded_rules),
    }
    extras = [
              IntegerRef("n", 1, 100),
              IntegerRef("minutes", 1, 720),
              Dictation("text"),
              Dictation("text2"),
              Dictation("text3"),
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
