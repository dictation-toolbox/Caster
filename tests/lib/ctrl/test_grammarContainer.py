from unittest import TestCase

from mock import Mock

from castervoice.lib.ctrl.mgr.grammar_container.basic_grammar_container import BasicGrammarContainer


class _FakeRule(object):
    def disable(self): pass


class _FakeGrammar(object):
    def __init__(self):
        self.rules = []

    def disable(self): pass

    def unload(self): pass


class TestGrammarContainer(TestCase):

    def setUp(self):
        self.rule1 = _FakeRule()
        self.rule1.disable = Mock()
        self.rule2 = _FakeRule()
        self.rule2.disable = Mock()
        self.grammar = _FakeGrammar()
        self.grammar.disable = Mock()
        self.grammar.unload = Mock()
        self.grammar.rules.extend([self.rule1, self.rule2])

    def test_set_ccr_update(self):
        gc = BasicGrammarContainer()
        gc.set_ccr([self.grammar])
        gc.set_ccr([_FakeGrammar()])

        self.rule1.disable.assert_called_with()
        self.rule2.disable.assert_called_with()
        self.grammar.disable.assert_called_with()
        self.grammar.unload.assert_called_with()

    def test_set_ccr_delete(self):
        gc = BasicGrammarContainer()
        gc.set_ccr([self.grammar])
        gc.set_ccr([])

        self.rule1.disable.assert_called_with()
        self.rule2.disable.assert_called_with()
        self.grammar.disable.assert_called_with()
        self.grammar.unload.assert_called_with()

    def test_set_non_ccr_update(self):
        gc = BasicGrammarContainer()
        gc.set_non_ccr("test", self.grammar)
        gc.set_non_ccr("test", _FakeGrammar())

        self.rule1.disable.assert_called_with()
        self.rule2.disable.assert_called_with()
        self.grammar.disable.assert_called_with()
        self.grammar.unload.assert_called_with()

    def test_set_non_ccr_delete(self):
        gc = BasicGrammarContainer()
        gc.set_non_ccr("test", self.grammar)
        gc.set_non_ccr("test", None)

        self.rule1.disable.assert_called_with()
        self.rule2.disable.assert_called_with()
        self.grammar.disable.assert_called_with()
        self.grammar.unload.assert_called_with()

    def test_wipe_ccr(self):
        gc = BasicGrammarContainer()
        gc.set_ccr = Mock()
        gc.wipe_ccr()
        gc.set_ccr.assert_called_with([])
