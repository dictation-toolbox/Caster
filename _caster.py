'''
main Caster module
'''

'''
Created on Jun 29, 2014

@author: dave

Instructions for adding new:
- homunculus windows in h_launch.py
- scanned languages (for "pita") in scanner.py
'''

from subprocess import Popen

from dragonfly import (Key, Function, Grammar, Playback,
                       IntegerRef, Dictation, Choice, Pause, MappingRule)



try:
    from caster.lib import settings# requires nothing
    from caster.lib import utilities# requires settings
    from caster.lib import control# requires settings
    from caster.lib.dfplus.state import stack# requires control
    
    from caster.apps import *
    from caster.asynch import *
    from caster.lib import ccr, context, recording
    from caster.asynch import auto_com
    import caster.dev, caster.wsr
    try:
        import caster.w
    except Exception:
        pass
    ccr.initialize_ccr()
    utilities.clean_temporary_files()
    recording.load_alias_rules()
    recording.load_recorded_rules()
    from caster.asynch.hmc import h_launch
    h_launch.clean_homunculi()
    if settings.SETTINGS["miscellaneous"]["status_window_enabled"] and not utilities.window_exists(None, statuswindow.TITLE):
        Popen(["pythonw", settings.SETTINGS["paths"]["STATUS_WINDOW_PATH"]])
    from caster.asynch.hmc import vocabulary_processing
    from caster.asynch.sikuli import sikuli
    from caster.lib import navigation, password
    from caster.lib.pita import scanner
    from caster.lib.dfplus.state.short import R
    from caster.lib.dfplus.hint import _nodes
except:
    import sys
    print sys.exc_info(), "\nAttempting to load CCR anyway..."
    from caster.lib import ccr
    ccr.initialize_ccr()



def fix_Dragon_double():
    try:
        lr = control.nexus().history[len(control.nexus().history) - 1]
        lu = " ".join(lr)
        Key("left/5:" + str(len(lu)) + ", del")._execute()
    except Exception:
        utilities.simple_log(False)
        
def repeat_that(n):
    try:
        if len(control.nexus().history) > 0:
            for i in range(int(n)):
                Playback([([str(x) for x in " ".join(control.nexus().history[len(control.nexus().history) - 1]).split()], 0.0)])._execute()
    except Exception:
        utilities.simple_log(False)

def change_monitor():
    if settings.SETTINGS["miscellaneous"]["sikuli_enabled"]:
        Playback([(["monitor", "select"], 0.0)])._execute()
    else:
        utilities.report("This command requires SikuliX to be enabled in the settings file")
       
class MainRule(MappingRule):
    
    @staticmethod
    def generate_CCR_choices():
        choices = {}
        for ccr_choice in settings.get_list_of_ccr_config_files():
            choices[settings.get_ccr_config_file_pronunciation(ccr_choice)] = ccr_choice
        return Choice("ccr_mode", choices)
    
    mapping = {
    # Dragon NaturallySpeaking management
    '(lock Dragon | deactivate)':   Playback([(["go", "to", "sleep"], 0.0)]),
    '(number|numbers) mode':        Playback([(["numbers", "mode", "on"], 0.0)]),
    'spell mode':                   Playback([(["spell", "mode", "on"], 0.0)]),
    'dictation mode':               Playback([(["dictation", "mode", "on"], 0.0)]),
    'normal mode':                  Playback([(["normal", "mode", "on"], 0.0)]),
    'com on':                       Playback([(["command", "mode", "on"], 0.0)]),
    'com off':                      Playback([(["command", "mode", "off"], 0.0)]),
    "reboot dragon":                R(Function(utilities.reboot), rdescript="Reboot Dragon Naturallyspeaking"),
    "fix dragon double":            R(Function(fix_Dragon_double), rdescript="Fix Dragon Double Letter"),
    "add word to vocabulary":       R(Function(vocabulary_processing.add_vocab), rdescript="Vocabulary Management: Add"),
    "delete word from vocabulary":  R(Function(vocabulary_processing.del_vocab), rdescript="Vocabulary Management: Delete"),
    
    # hardware management
    "volume <volume_mode> [<n>]":   Function(navigation.volume_control, extra={'n', 'volume_mode'}),
    "change monitor":               Key("w-p") + Pause("100") + Function(change_monitor),
    
    # window management
    'minimize':                     Playback([(["minimize", "window"], 0.0)]),
    'maximize':                     Playback([(["maximize", "window"], 0.0)]),
    "remax":                        R(Key("a-space/10,r/10,a-space/10,x"), rdescript="Force Maximize"),
        
    # passwords
    'hash password <text> <text2> <text3>':                    R(Function(password.hash_password), rdescript="Get Hash Password"),
    'get password <text> <text2> <text3>':                     R(Function(password.get_password), rdescript="Get Seed Password"),
    'get restricted password <text> <text2> <text3>':          R(Function(password.get_restricted_password), rdescript="Get Char-Restricted Password"),
    'quick pass <text> <text2> <text3>':                       R(Function(password.get_simple_password), rdescript="Get Crappy Password"),
    
    # mouse alternatives
    "legion":                       R(Function(navigation.mouse_alternates, mode="legion"), rdescript="Activate Legion"),
    "rainbow":                      R(Function(navigation.mouse_alternates, mode="rainbow"), rdescript="Activate Rainbow Grid"),
    "douglas":                      R(Function(navigation.mouse_alternates, mode="douglas"), rdescript="Activate Douglas Grid"),
    
    # pita (fuzzy string matching)
    "scan directory":               R(Function(scanner.scan_directory), rdescript="Scan Directory For PITA"),
    "rescan current":               R(Function(scanner.rescan_current_file), rdescript="Rescan Current File For PITA"),
    
    # macro recording and automation
    "record from history":          R(Function(recording.record_from_history), rdescript="Create Macro From Spoken"),
    "delete recorded macros":       R(Function(recording.delete_recorded_rules), rdescript="Delete Recorded Macros"),
    "wait sec [<n>]":               R(Pause("%(n)d00"), rdescript="Wait (Macro Recording)"),
    
    # aliasing
    "alias <text>":                 R(Function(recording.add_alias), rdescript="Create Alias Command"),
    "delete aliases":               R(Function(recording.delete_alias_rules), rdescript="Delete All Alias Commands"),
    "chain alias":                  R(Function(recording.get_chain_alias_spec), rdescript="Create CCR Alias Command"), 
    
    # miscellaneous
    "<enable_disable> <ccr_mode>":  R(Function(ccr.set_active_command), rdescript="Enable CCR Module"),
    "refresh <ccr_mode>":           R(Function(ccr.refresh_from_files), rdescript="Refresh CCR Module"), 
    "again (<n> [(times|time)] | do)":R(Function(repeat_that), rdescript="Repeat Last Action"),
    
    }
    extras = [
              IntegerRef("n", 1, 50),
              Dictation("text"),
              Dictation("text2"),
              Dictation("text3"),
              Choice("enable_disable",
                    {"enable": 1, "disable": 0
                    }),
              Choice("volume_mode",
                    {"mute": "mute", "up":"up", "down":"down"
                     }),
              generate_CCR_choices.__func__()
             ]
    defaults = {"n": 1, "nnv": 1,
               "text": "", "volume_mode": "setsysvolume",
               "enable":-1
               }


grammar = Grammar('general')
grammar.add_rule(MainRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
    ccr.unload()
    sikuli.unload()
