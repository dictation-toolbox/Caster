from unittest import TestCase

from castervoice.lib.merge.ccrmerging2.compatibility.detail_compat_checker import DetailCompatibilityChecker
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.actions2 import NullAction


class _TestRuleA(MergeRule):
    mapping = {
        "spec one": NullAction()
    }


class _TestRuleB(MergeRule):
    mapping = {
        "spec two": NullAction()
    }


class _TestRuleC(MergeRule):
    mapping = {
        "spec one": NullAction(),
        "spec two": NullAction()
    }


class TestDetailCompatibilityChecker(TestCase):

    def setUp(self):
        self.compat_checker = DetailCompatibilityChecker()

    def test_no_incompatibilities_between_compatible_rules(self):
        result = self.compat_checker.compatibility_check([_TestRuleA(), _TestRuleB()])
        a_incompats = self._get_incompatible_set_for_rule_class(result, "_TestRuleA")
        b_incompats = self._get_incompatible_set_for_rule_class(result, "_TestRuleB")
        self.assertEqual(0, len(a_incompats))
        self.assertEqual(0, len(b_incompats))

    def test_incompatibilities_detected_between_pairs(self):
        result = self.compat_checker.compatibility_check([_TestRuleA(), _TestRuleC()])
        a_incompats = self._get_incompatible_set_for_rule_class(result, "_TestRuleA")
        c_incompats = self._get_incompatible_set_for_rule_class(result, "_TestRuleC")
        self.assertEqual(1, len(a_incompats))
        self.assertIn("_TestRuleC", a_incompats)
        self.assertEqual(1, len(c_incompats))
        self.assertIn("_TestRuleA", c_incompats)
        result = self.compat_checker.compatibility_check([_TestRuleB(), _TestRuleC()])
        b_incompats = self._get_incompatible_set_for_rule_class(result, "_TestRuleB")
        c_incompats = self._get_incompatible_set_for_rule_class(result, "_TestRuleC")
        self.assertEqual(1, len(b_incompats))
        self.assertIn("_TestRuleC", b_incompats)
        self.assertEqual(1, len(c_incompats))
        self.assertIn("_TestRuleB", c_incompats)

    def test_incompatibilities_detected_between_triple(self):
        result = self.compat_checker.compatibility_check([_TestRuleA(), _TestRuleB(), _TestRuleC()])
        a_incompats = self._get_incompatible_set_for_rule_class(result, "_TestRuleA")
        b_incompats = self._get_incompatible_set_for_rule_class(result, "_TestRuleB")
        c_incompats = self._get_incompatible_set_for_rule_class(result, "_TestRuleC")
        self.assertEqual(1, len(a_incompats))
        self.assertIn("_TestRuleC", a_incompats)
        self.assertEqual(1, len(b_incompats))
        self.assertIn("_TestRuleC", b_incompats)
        self.assertEqual(2, len(c_incompats))
        self.assertIn("_TestRuleB", c_incompats)
        self.assertIn("_TestRuleA", c_incompats)

    def _get_incompatible_set_for_rule_class(self, compat_result, rcn):
        for cr in compat_result:
            if cr.rule_class_name() == rcn:
                return cr.incompatible_rule_class_names()
        raise Exception(rcn + " not found")
