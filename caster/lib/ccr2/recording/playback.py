'''
Created on Sep 3, 2015

@author: synkarius
'''
import re

from dragonfly.actions.action_playback import Playback
from dragonfly.language.base.integer import IntegerRef

from caster.asynch.hmc import h_launch
from caster.lib import control, settings, utilities
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.mergerule import MergeRule
from caster.lib.dfplus.state.actions2 import NullAction
from caster.lib.dfplus.state.short import R


class PlaybackRule(MergeRule):
    
    mapping = {
        "default sequence":       NullAction(), 
        }
    
    
    def record_from_history(self):
        # save the list as it was when the command was spoken
        control.nexus().preserved = control.nexus().history[:]
        
        # format for display
        formatted = ""
        for t in control.nexus().preserved:
            for w in t:
                formatted += w.split("\\")[0] + "[w]"
            formatted += "[s]"
        
        def callback(data):
            self.add_recorded_macro(data)
        # use a response window to get a spec and word sequences for the new macro
        h_launch.launch(settings.QTYPE_RECORDING, callback, formatted)
        
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
            self.refresh((spec, word_sequences))
            
        
        
    
    def refresh(self, new_entry=None):
        '''new_entry is a tuple: (spec, list of lists of strings)'''
        
        # get mapping
        recorded_macros = utilities.load_json_file(settings.SETTINGS["paths"]["RECORDED_MACROS_PATH"])
        if new_entry!=None:
            recorded_macros[new_entry[0]] = new_entry[1]
            utilities.save_json_file(recorded_macros, settings.SETTINGS["paths"]["RECORDED_MACROS_PATH"])
        mapping = {}
        for spec, sequences in recorded_macros:
            mapping[spec] = R(Playback([(sequence, 0.0) for sequence in sequences]), rdescript="Recorded Macro: "+spec)
        if len(mapping)==0: mapping = PlaybackRule.mapping
        
        # reload with new mapping
        control.nexus().ccr_grammar.unload()
        MergeRule.__init__(self, self.name, mapping, extras=[IntegerRefST("n", 1, 50)], defaults={"n":1})
        # TODO: compatibility checking here?
        control.nexus().ccr_grammar.load()
    
    def load_recorded_macros(self):
        self.refresh()
    
    def delete_recorded_macros(self):
        utilities.save_json_file({}, settings.SETTINGS["paths"]["RECORDED_MACROS_PATH"])
        self.refresh()
    
    