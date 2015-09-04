'''
Created on Sep 3, 2015

@author: synkarius
'''
from caster.lib.dfplus.mergerule import MergeRule
from caster.lib.dfplus.state.actions2 import NullAction


class PlaybackRule(MergeRule):
    mapping = {
        "default sequence":       NullAction(), 
        }