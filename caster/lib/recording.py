import os
import time

from dragonfly import (Playback, CompoundRule, IntegerRef, Mimic, Text)

from caster.asynch.hmc import h_launch
from caster.lib import settings, control, utilities, navigation, context, ccr


MESSAGE_SPLITTER = "<chain_alias>"

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

def add_alias(text):
    text = str(text)
    if text == "":
        return
    alias_key = "alias_key"    
    navigation.clipboard_to_file(alias_key, True)
    time.sleep(0.1)
    symbol = control.nexus().clip[alias_key]
    rewrite_alias_module(None, (str(text), symbol))
    ccr.refresh_from_files("aliases")

def rewrite_alias_module(ccr_, non_):
    '''
    ccr_, non_ are tuples in the form (spec, text), and are nullable
    '''
    add = ccr_ != None or non_ != None
    ccr_open = False
    non_open = False
    written = False
    exists = os.path.isfile(settings.SETTINGS["paths"]["ALIASES_PATH"])
    lines = []
    
    if not add or not exists:
        lines = ccr.MODULE_SHELL
    else:
        # read in the file
        try:
            with open(settings.SETTINGS["paths"]["ALIASES_PATH"], "r+") as f:
                lines = f.readlines()
        except Exception:
            utilities.simple_log(True)
    
    try:
        with open(settings.SETTINGS["paths"]["ALIASES_PATH"], "w+") as f:
            for line in lines:
                if line.isspace():
                    continue
                if ccr.MODULE_MARKERS[0] in line: ccr_open = True
                elif ccr.MODULE_MARKERS[1] in line: ccr_open = False
                elif ccr.MODULE_MARKERS[2] in line: non_open = True
                elif ccr.MODULE_MARKERS[3] in line: non_open = False
                
#                 print str(add), str(ccr_open), str(non_open), str(written) 
                
                f.write(line + "\n")
                if add:
                    if not written: 
                        if (ccr_open and ccr_ != None) or (non_open and non_ != None):
                            a = ccr_ if ccr_open else non_
                            f.write("'" + a[0] + "': Text('" + a[1] + "'),")
                            written = True
    except Exception:
        utilities.simple_log(True)

def load_alias_rules():
    if not os.path.isfile(settings.SETTINGS["paths"]["ALIASES_PATH"]):
        rewrite_alias_module(None, None)

def delete_alias_rules():
    rewrite_alias_module(None, None)
    ccr.refresh_from_files("aliases")

def get_chain_alias_spec():
    global MESSAGE_SPLITTER
    result=None
    copy_worked=False
    for i in range(0, 10):
        result=context.read_selected_without_altering_clipboard(True)
        if result[0]==0:
            copy_worked=True
            break
    if copy_worked==True:
        h_launch.launch(settings.QTYPE_INSTRUCTIONS, chain_alias, "Enter_spec_for_command|" + MESSAGE_SPLITTER.join(result[1].split()))
    else:
        utilities.report("copy failed") 

def chain_alias(data):
    global MESSAGE_SPLITTER
    ''''''
    spec = data[0].replace("\n", "")
    text = " ".join(data[1].split(MESSAGE_SPLITTER))
    rewrite_alias_module((spec, text), None)
    ccr.refresh_from_files("aliases")

def get_macro_spec(): 
    h_launch.launch(settings.QTYPE_DEFAULT, add_recorded_macro, None)

def record_from_history():
    # save the list as it was when the command was spoken
    control.nexus().preserved = control.nexus().history[:]
    
    # format for display
    formatted = ""
    for t in control.nexus().preserved:
        for w in t:
            formatted += w.split("\\")[0] + "[w]"
        formatted += "[s]"
    
    h_launch.launch(settings.QTYPE_RECORDING, add_recorded_macro, formatted)
    

def add_recorded_macro(data):
    # use a response window to get a spec for the new macro: handled by calling function
    commands = []
    for i in data["selected_indices"]:
        commands.append(control.nexus().preserved[i])
    
    
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
        control.nexus().macros_grammar.unload()
        rule = RecordedRule(commands=commands, spec=spec, name="recorded_rule_" + spec, extras=extras, defaults=defaults)
        control.nexus().macros_grammar.add_rule(rule)
        control.nexus().macros_grammar.load()
    
    # clear the dictation cache
    control.nexus().preserved = None

def load_recorded_rules():
    recorded_macros = utilities.load_json_file(settings.SETTINGS["paths"]["RECORDED_MACROS_PATH"])
    for spec in recorded_macros:
        commands = recorded_macros[spec]# this is a list of lists
        rule = RecordedRule(commands=commands, spec=spec, name="recorded_rule_" + spec, extras=[IntegerRef("n", 1, 50)], defaults={"n":1})
        control.nexus().macros_grammar.add_rule(rule)
    if len(control.nexus().macros_grammar.rules) > 0:
        control.nexus().macros_grammar.load()

def delete_recorded_rules():
    utilities.save_json_file({}, settings.SETTINGS["paths"]["RECORDED_MACROS_PATH"])
    control.nexus().macros_grammar.unload()
    while len(control.nexus().macros_grammar.rules) > 0:
        rule = control.nexus().macros_grammar.rules[0]
        control.nexus().macros_grammar.remove_rule(rule)
