from dragonfly.actions.action_focuswindow import FocusWindow
from dragonfly.actions.action_key import Key
from dragonfly.actions.action_playback import Playback
from dragonfly.actions.action_waitwindow import WaitWindow
from dragonfly.grammar.rule_compound import CompoundRule

from asynch.hmc import h_launch, squeue
from lib import settings, control


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

def add_recorded_macro(data):
    ''''''
    # use a response window to get a spec for the new macro: handled by calling function
    
    # search through dictation cache for "begin recording macro"
    beginning_found = False
    commands = []
    
    for i in range(0, len(control.DICTATION_CACHE)):
        d = control.DICTATION_CACHE[i]
        if not beginning_found:
            if d[0] == "begin" and d[1] == "recording":
                beginning_found = True
            continue
        
        if d[0] == "end" and d[1] == "recording":
            break
        # take every tuple after that  and turn it into a comma separated list
        commands.append(list(d))
    
    spec = data
    # clean the results
    for l in commands:
        for w in l:
            if "\\" in w:
                w = w.split("\\")[0]
    spec = spec.replace("\n", "") 
    
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
    while len(control.DICTATION_CACHE) > 0:
        control.DICTATION_CACHE.pop()


def null_func():
    '''this function intentionally does nothing, is for use with macro recording'''

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