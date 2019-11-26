class FakeGrammarContainer(object):
    """
    A spy for the grammar container.
    """

    def __init__(self):
        self.ccr = []
        self.non_ccr = {}

    def _pass(self):
        pass

    def set_non_ccr(self, rcn, grammar):
        if grammar is not None:
            grammar.load = lambda: self._pass()
            self.non_ccr[rcn] = grammar
        else:
            del self.non_ccr[rcn]

    def set_ccr(self, ccr_grammars):
        for grammar in ccr_grammars:
            grammar.load = lambda: self._pass()

        self.ccr = ccr_grammars

    def wipe_ccr(self):
        pass
