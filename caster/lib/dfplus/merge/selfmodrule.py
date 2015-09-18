'''
Created on Sep 6, 2015

@author: synkarius
'''
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.actions2 import NullAction
from dragonfly.grammar.elements import Dictation


class SelfModifyingRule(MergeRule):
    '''
    SelfModifyingRule is a kind of rule which gets its command set changed
    on-the-fly based on some kind of user interaction. Child classes
    must implement their own version of the `refresh` method.
    '''
    
    def refresh(self, *args):
        '''Does stuff to get mapping, then calls self.reset()'''
        self.reset({ "default record rule spec": NullAction() })
    
    def reset(self, mapping):
        grammar = self.grammar # save reference because Grammar.remove_rule nullifies it
        grammar.unload() 
        grammar.remove_rule(self)
        MergeRule.__init__(self, self.name, mapping, 
                           extras=[IntegerRefST("n", 1, 50), Dictation("s")], 
                           defaults={"n":1})
        grammar.add_rule(self)
        grammar.load()