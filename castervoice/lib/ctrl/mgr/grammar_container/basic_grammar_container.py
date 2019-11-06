from castervoice.lib.ctrl.mgr.grammar_container.base_grammar_container import BaseGrammarContainer


class BasicGrammarContainer(BaseGrammarContainer):
    """
    Responsible for holding and destroying
    CCR and non-CCR grammars.
    """

    def __init__(self):
        """
        ccr grammars ALL get wiped every merge = list
        non-ccr grammars get turned on/off one at a time = dict
        """
        self._ccr_grammars = []
        self._non_ccr_grammars = {}

    def set_non_ccr(self, rcn, grammar):
        if rcn in self._non_ccr_grammars:
            old_grammar = self._non_ccr_grammars[rcn]
            BasicGrammarContainer._empty_grammar(old_grammar)
            del self._non_ccr_grammars[rcn]

        if grammar is not None:
            self._non_ccr_grammars[rcn] = grammar

    def set_ccr(self, ccr_grammars):
        # first, wipe out old ccr rules
        for ccr_grammar in self._ccr_grammars:
            BasicGrammarContainer._empty_grammar(ccr_grammar)
        self._ccr_grammars = ccr_grammars

    def wipe_ccr(self):
        self.set_ccr([])

    @staticmethod
    def _empty_grammar(grammar):
        # disable all of the grammar's rules
        for rule in grammar.rules:
            rule.disable()
        # disable / unload grammar
        grammar.disable()
        grammar.unload()
