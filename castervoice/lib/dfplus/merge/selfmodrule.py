'''
Created on Sep 6, 2015

@author: synkarius
'''
from dragonfly.grammar.elements import Dictation

from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge.mergepair import MergeInf
from castervoice.lib.dfplus.merge.mergerule import MergeRule

class SelfModifyingRule(MergeRule):
    '''
    SelfModifyingRule is a kind of rule which gets its command set changed
    on-the-fly based on some kind of user interaction. Child classes
    must implement their own version of the `refresh` method.
    '''

    def __init__(self,
                 name=None,
                 mapping=None,
                 extras=None,
                 defaults=None,
                 exported=None,
                 refresh=True):
        MergeRule.__init__(self, name, mapping, extras, defaults, exported)
        self._merger = None
        if refresh: self.refresh()

    def refresh(self, *args):
        '''Does stuff to get mapping, then calls self.reset()'''
        raise NotImplementedError()

    def set_merger(self, merger):
        '''only set for CCR SelfModifyingRules'''
        self._merger = merger

    def reset(self, mapping):
        grammar = self._grammar  # save reference because Grammar.remove_rule nullifies it
        ccr = self._merger is not None

        if grammar is not None and not ccr:
            grammar.unload()
            grammar.remove_rule(self)

        extras = self.extras if self.extras else [IntegerRefST("n", 1, 50), Dictation("s")]
        defaults = self.defaults if self.defaults else { "n": 1, "s": "" }
        MergeRule.__init__(self, self.name, mapping, extras, defaults, self.exported,
                           self.context)

        if ccr: self._merger.merge(MergeInf.SELFMOD)

        if grammar is not None and not ccr:
            grammar.add_rule(self)
            grammar.load()
