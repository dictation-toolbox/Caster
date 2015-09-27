'''
Created on Sep 3, 2015

@author: synkarius
'''
from dragonfly.actions.action_base import Repeat
from dragonfly.actions.action_function import Function
from dragonfly.actions.action_playback import Playback

from caster.asynch.hmc import h_launch
from caster.lib import control, settings, utilities
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge.selfmodrule import SelfModifyingRule
from caster.lib.dfplus.state.actions2 import NullAction
from caster.lib.dfplus.state.short import R


class HistoryRule(SelfModifyingRule):
    pronunciation = "history"
    mapping = {"default sequence":  NullAction()}
    
    def record_from_history(self):
        # save the list as it was when the command was spoken
        control.nexus().preserved = control.nexus().history[:]
        
        # format for display
        formatted = ""
        for t in control.nexus().preserved:
            for w in t:
                formatted += w.split("\\")[0] + "[w]"
            formatted += "[s]"
        
        # use a response window to get a spec and word sequences for the new macro
        h_launch.launch(settings.QTYPE_RECORDING, lambda data: self.add_recorded_macro(data), formatted)
        
    def add_recorded_macro(self, data):
        spec = data["word"]
        
        word_sequences = [] # word_sequences is a list of lists of strings
        for i in data["selected_indices"]:
            single_sequence = control.nexus().preserved[i]
            # clean the results
            for k in range(0,len(single_sequence)):
                if "\\" in single_sequence[k]:
                    single_sequence[k] = single_sequence[k].split("\\")[0]
            word_sequences.append(single_sequence)
        
        # clear the dictation cache
        control.nexus().preserved = None
        
        if spec != "" and len(word_sequences) > 0:
            if data["repeatable"]:
                spec += " [times <n>]"
            self.refresh(spec, word_sequences)
        
    
    def refresh(self, *args):
        '''args: spec, list of lists of strings'''
        
        # get mapping
        recorded_macros = utilities.load_json_file(settings.SETTINGS["paths"]["RECORDED_MACROS_PATH"])
        if len(args)>0:
            recorded_macros[args[0]] = args[1]
            utilities.save_json_file(recorded_macros, settings.SETTINGS["paths"]["RECORDED_MACROS_PATH"])
        mapping = {}
        for spec in recorded_macros:
            sequences = recorded_macros[spec]
            mapping[spec] = R(Playback([(sequence, 0.0) for sequence in sequences])*Repeat(extra="n"), rdescript="Recorded Macro: "+spec)
        mapping["record from history"] = R(Function(self.record_from_history), rdescript="Record From History")
        mapping["delete recorded macros"] = R(Function(self.delete_recorded_macros), rdescript="Delete Recorded Macros")
        # reload with new mapping
        self.reset(mapping)
    
    def load_recorded_macros(self):
        self.refresh()
    
    def delete_recorded_macros(self):
        utilities.save_json_file({}, settings.SETTINGS["paths"]["RECORDED_MACROS_PATH"])
        self.refresh()
    
control.nexus().merger.add_selfmodrule(HistoryRule())