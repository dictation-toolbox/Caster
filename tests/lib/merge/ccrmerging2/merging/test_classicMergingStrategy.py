from unittest import TestCase

from castervoice.lib.merge.ccrmerging2.compatibility.compat_result import CompatibilityResult
from castervoice.lib.merge.ccrmerging2.merging.classic_merging_strategy import ClassicMergingStrategy
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.actions2 import NullAction


class _TestRuleA(MergeRule):
    mapping = {
        "hello": NullAction(),
        "a": NullAction()
    }


class _TestRuleB(MergeRule):
    mapping = {
        "hello": NullAction(),
        "b": NullAction()
    }


class TestClassicMergingStrategy(TestCase):
    """
    Higher index in '_enabled_ordered' wins in rule conflicts.
    """

    def setUp(self):
        self.merge_strategy = ClassicMergingStrategy()
        self.compat_results_ab = [
            CompatibilityResult(_TestRuleA(), set(["_TestRuleB"])),
            CompatibilityResult(_TestRuleB(), set(["_TestRuleA"]))
        ]
        self.compat_results_ba = [
            CompatibilityResult(_TestRuleB(), set(["_TestRuleA"])),
            CompatibilityResult(_TestRuleA(), set(["_TestRuleB"]))
        ]

    def test_a_knocks_out_b(self):
        merged_rule = self.merge_strategy.merge_into_single(self.compat_results_ba)
        self.assertIn("a", merged_rule.get_mapping().keys())

    def test_b_knocks_out_a(self):
        merged_rule = self.merge_strategy.merge_into_single(self.compat_results_ab)
        self.assertIn("b", merged_rule.get_mapping().keys())
