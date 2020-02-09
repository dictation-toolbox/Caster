from unittest import TestCase

from castervoice.lib.merge.ccrmerging2.compatibility.simple_compat_checker import SimpleCompatibilityChecker
from tests.lib.merge.ccrmerging2.fake_rules import FakeRuleOne, FakeRuleTwo, FakeRuleThree


class TestSimpleCompatibilityChecker(TestCase):

    def setUp(self):
        self._compat_checker = SimpleCompatibilityChecker()

    def test_elimination(self):
        a = FakeRuleOne()
        b = FakeRuleTwo()
        rules = [a, b]
        results = self._compat_checker.compatibility_check(rules)
        self.assertEqual(1, len(results))
        self.assertIs(b, results[0].rule())

    def test_order_preservation(self):
        a = FakeRuleOne()
        b = FakeRuleThree()

        rules = [a, b]
        results = self._compat_checker.compatibility_check(rules)
        self.assertIs(a, results[0].rule())
        self.assertIs(b, results[1].rule())

        rules = [b, a]
        results = self._compat_checker.compatibility_check(rules)
        self.assertIs(b, results[0].rule())
        self.assertIs(a, results[1].rule())
