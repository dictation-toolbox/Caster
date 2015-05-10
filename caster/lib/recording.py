import time

from dragonfly import (Playback, CompoundRule, IntegerRef, Mimic, Text)

from caster.asynch.hmc import h_launch
from caster.lib import settings, control, utilities, navigation


class RecordedRule(CompoundRule):
    def __init__(self, commands, name=None, spec=None, extras=None,
        defaults=None, exported=None, context=None):
        CompoundRule.__init__(self, name=name, spec=spec, extras=extras, defaults=defaults, exported=exported, context=context)
        self.playback_array = []
        for command in commands:
            self.playback_array.append((command, 0.05))
            
    def _process_recognition(self, node, extras):
        if "n" in extras:
            for i in range(0, int(extras["n"])):
                Playback(self.playback_array)._execute()
        else:
            Playback(self.playback_array)._execute()

class AliasRule(CompoundRule):
    def __init__(self, symbol, name=None, spec=None, extras=None,
        defaults=None, exported=None, context=None):
        CompoundRule.__init__(self, name=name, spec=spec, extras=extras, defaults=defaults, exported=exported, context=context)
        self._symbol = symbol
            
    def _process_recognition(self, node, extras):
        Text(self._symbol).execute()

def add_alias(text):
    text = str(text)
    if text == "":
        return
    alias_key = "alias_key"
    utilities.report(1)
    
    navigation.clipboard_to_file(alias_key, True)
    time.sleep(0.1)
    symbol = control.MULTI_CLIPBOARD[alias_key]
    control.ALIASES_GRAMMAR.unload()
    rule = AliasRule(symbol=symbol, spec=str(text), name="alias_rule_" + text)
    if len(control.ALIASES_GRAMMAR._rules)>0:
        control.ALIASES_GRAMMAR._rules = [x for x in control.ALIASES_GRAMMAR._rules if x._name != rule._name]
    control.ALIASES_GRAMMAR.add_rule(rule)
    control.ALIASES_GRAMMAR.load()
    aliases = utilities.load_json_file(settings.SETTINGS["paths"]["ALIASES_PATH"])
    aliases[str(text)] = symbol
    utilities.save_json_file(aliases, settings.SETTINGS["paths"]["ALIASES_PATH"])

def load_alias_rules():
    aliases = utilities.load_json_file(settings.SETTINGS["paths"]["ALIASES_PATH"])
    if len(aliases) > 0:
        control.ALIASES_GRAMMAR.unload()
        for text in aliases:
            symbol = aliases[text]
            rule = AliasRule(symbol=symbol, spec=str(text), name="alias_rule_" + str(text))
            control.ALIASES_GRAMMAR.add_rule(rule)
        control.ALIASES_GRAMMAR.load()

def delete_alias_rules():
    utilities.save_json_file({}, settings.SETTINGS["paths"]["ALIASES_PATH"])
    control.ALIASES_GRAMMAR.unload()
    while len(control.ALIASES_GRAMMAR.rules) > 0:
        rule = control.ALIASES_GRAMMAR.rules[0]
        control.ALIASES_GRAMMAR.remove_rule(rule)

def get_macro_spec(): 
    h_launch.launch(settings.QTYPE_DEFAULT, add_recorded_macro, None)

def record_from_history():
    # save the list as it was when the command was spoken
    control.PRESERVED_CACHE = control.DICTATION_CACHE[:]
    
    # format for display
    formatted = ""
    for t in control.PRESERVED_CACHE:
        for w in t:
            formatted += w.split("\\")[0] + "[w]"
        formatted += "[s]"
    
    h_launch.launch(settings.QTYPE_RECORDING, add_recorded_macro, formatted)
    

def add_recorded_macro(data):
    # use a response window to get a spec for the new macro: handled by calling function
    commands = []
#     print control.PRESERVED_CACHE
    for i in data["selected_indices"]:
#         print i, ":", control.PRESERVED_CACHE[i]
        commands.append(control.PRESERVED_CACHE[i])
    
    
    spec = data["word"]
    # clean the results
    for l in commands:
        for w in l:
            if "\\" in w:
                w = w.split("\\")[0]
    
    recorded_macros = None
    if spec != "" and len(commands) > 0:
        extras = None
        defaults = None
        if data["repeatable"]:
            spec += " [times <n>]"
            extras = [IntegerRef("n", 1, 50)]
            defaults = {"n":1}
        
        recorded_macros = utilities.load_json_file(settings.SETTINGS["paths"]["RECORDED_MACROS_PATH"])
        recorded_macros[spec] = commands
        utilities.save_json_file(recorded_macros, settings.SETTINGS["paths"]["RECORDED_MACROS_PATH"])
        
        # immediately make a new compound rule  and add to a set grammar
        control.RECORDED_MACROS_GRAMMAR.unload()
        rule = RecordedRule(commands=commands, spec=spec, name="recorded_rule_" + spec, extras=extras, defaults=defaults)
        control.RECORDED_MACROS_GRAMMAR.add_rule(rule)
        control.RECORDED_MACROS_GRAMMAR.load()
    
    # clear the dictation cache
    control.PRESERVED_CACHE = None

def load_recorded_rules():
    recorded_macros = utilities.load_json_file(settings.SETTINGS["paths"]["RECORDED_MACROS_PATH"])
    for spec in recorded_macros:
        commands = recorded_macros[spec]
        rule = RecordedRule(commands=commands, spec=spec, name="recorded_rule_" + spec, extras=[IntegerRef("n", 1, 50)], defaults={"n":1})
        control.RECORDED_MACROS_GRAMMAR.add_rule(rule)
    if len(control.RECORDED_MACROS_GRAMMAR.rules) > 0:
        control.RECORDED_MACROS_GRAMMAR.load()

def delete_recorded_rules():
    utilities.save_json_file({}, settings.SETTINGS["paths"]["RECORDED_MACROS_PATH"])
    control.RECORDED_MACROS_GRAMMAR.unload()
    while len(control.RECORDED_MACROS_GRAMMAR.rules) > 0:
        rule = control.RECORDED_MACROS_GRAMMAR.rules[0]
        control.RECORDED_MACROS_GRAMMAR.remove_rule(rule)
