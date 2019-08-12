class GrammarContainer(object):
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

    def set_non_ccr(self, rule_class_name, grammar):
        if rule_class_name in self._non_ccr_grammars:
            grammar = self._non_ccr_grammars[rule_class_name]
            GrammarContainer._empty_grammar(grammar)
            del self._non_ccr_grammars[rule_class_name]

        if grammar is not None:
            self._non_ccr_grammars[rule_class_name] = grammar

    def set_ccr(self, ccr_grammars):
        # first, wipe out old ccr rules
        for ccr_grammar in self._ccr_grammars:
            GrammarContainer._empty_grammar(ccr_grammar)
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
