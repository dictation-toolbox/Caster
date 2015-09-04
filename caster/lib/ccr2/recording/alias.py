'''
Created on Sep 3, 2015

@author: synkarius
'''
from caster.lib.dfplus.mergerule import MergeRule
from caster.lib.dfplus.state.actions2 import NullAction


class AliasesNon(MergeRule):
    mapping = {
        "default command":       NullAction(), 
        }

class Aliases(MergeRule):
    non = AliasesNon
    
    mapping = {
        "default command":       NullAction(), 
        }