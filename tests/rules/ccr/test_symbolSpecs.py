from unittest import TestCase

from castervoice.rules.ccr.standard import SymbolSpecs


class TestSymbolSpecs(TestCase):
    def test_set_cancel_word(self):
        SymbolSpecs.set_cancel_word("test")
        self.assertEqual("test", SymbolSpecs.CANCEL)
