class FakeGrammarContainer(object):
    """
    This is a test class. It should be in the test packages.
    """

    def _pass(self):
        pass

    def set_non_ccr(self, rcn, grammar):
        grammar.load = lambda: self._pass()

    def set_ccr(self, ccr_grammars):
        for grammar in ccr_grammars:
            grammar.load = lambda: self._pass()

    def wipe_ccr(self):
        pass
