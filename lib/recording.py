from dragonfly.actions.action_focuswindow import FocusWindow
from dragonfly.actions.action_key import Key
from dragonfly.actions.action_playback import Playback
from dragonfly.actions.action_waitwindow import WaitWindow
from dragonfly.grammar.rule_compound import CompoundRule

from asynch.hmc import h_launch, squeue
from lib import settings, control, utilities


class RecordedRule(CompoundRule):
    def __init__(self, commands, name=None, spec=None, extras=None,
        defaults=None, exported=None, context=None):
        CompoundRule.__init__(self, name=name, spec=spec, extras=extras, defaults=defaults, exported=exported, context=context)
        self.playback_array = []
        for command in commands:
            self.playback_array.append((command, 0.05))
            
    def _process_recognition(self, node, extras):
        Playback(self.playback_array)._execute()

def get_macro_spec():
    ''''''
    h_launch.launch(settings.QTYPE_DEFAULT)
    WaitWindow(title=settings.HOMUNCULUS_VERSION, timeout=5)._execute()
    FocusWindow(title=settings.HOMUNCULUS_VERSION)._execute()
    Key("tab")._execute()
    squeue.add_query(add_recorded_macro)

def record_from_history():
    # save the list as it was when the command was spoken
    control.PRESERVED_CACHE = control.DICTATION_CACHE[:]
    
    # format for display
    formatted = ""
    for t in control.PRESERVED_CACHE:
        for w in t:
            formatted += w.split("\\")[0] + "[w]"
        formatted += "[s]"
    
    h_launch.launch(settings.QTYPE_RECORDING, formatted)
    WaitWindow(title=settings.HOMUNCULUS_VERSION + settings.HMC_TITLE_RECORDING, timeout=5)._execute()
    FocusWindow(title=settings.HOMUNCULUS_VERSION + settings.HMC_TITLE_RECORDING)._execute()
    Key("tab")._execute()
    squeue.add_query(add_recorded_macro)
    

def add_recorded_macro(data):
    # use a response window to get a spec for the new macro: handled by calling function
    commands = []
    print control.PRESERVED_CACHE
    for i in data["selected_indices"]:
        print i, ":", control.PRESERVED_CACHE[i]
        commands.append(control.PRESERVED_CACHE[i])
    
    
    spec = data["word"]
    # clean the results
    for l in commands:
        for w in l:
            if "\\" in w:
                w = w.split("\\")[0]
    
    # store the list in the macros section of the settings file
    recorded_macros = None
    if spec != "" and len(commands) > 0:
        recorded_macros = settings.load_json_file(settings.SETTINGS["paths"]["RECORDED_MACROS_PATH"])
        recorded_macros[spec] = commands
        settings.save_json_file(recorded_macros, settings.SETTINGS["paths"]["RECORDED_MACROS_PATH"])
    
    # immediately make a new compound rule  and add to a set grammar
    control.RECORDED_MACROS_GRAMMAR.unload()
    rule = RecordedRule(commands=commands, spec=spec, name="recorded_rule_" + spec)
    control.RECORDED_MACROS_GRAMMAR.add_rule(rule)
    control.RECORDED_MACROS_GRAMMAR.load()
    
    # clear the dictation cache
    control.PRESERVED_CACHE = None


def load_recorded_rules():
    recorded_macros = settings.load_json_file(settings.SETTINGS["paths"]["RECORDED_MACROS_PATH"])
    for spec in recorded_macros:
        commands = recorded_macros[spec]
        rule = RecordedRule(commands=commands, spec=spec, name="recorded_rule_" + spec)
        control.RECORDED_MACROS_GRAMMAR.add_rule(rule)
    if len(control.RECORDED_MACROS_GRAMMAR.rules) > 0:
        control.RECORDED_MACROS_GRAMMAR.load()

def delete_recorded_rules():
    settings.save_json_file({}, settings.SETTINGS["paths"]["RECORDED_MACROS_PATH"])
    control.RECORDED_MACROS_GRAMMAR.unload()
    while len(control.RECORDED_MACROS_GRAMMAR.rules) > 0:
        rule = control.RECORDED_MACROS_GRAMMAR.rules[0]
        control.RECORDED_MACROS_GRAMMAR.remove_rule(rule)
