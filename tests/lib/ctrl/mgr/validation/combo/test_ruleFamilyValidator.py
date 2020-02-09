from unittest import TestCase

from dragonfly import MappingRule, CompoundRule

from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.ctrl.mgr.validation.combo.rule_family_validator import RuleFamilyValidator
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.selfmod.selfmodrule import BaseSelfModifyingRule


class _TestMappingRule(MappingRule):
    pass


class _TestMergeRule(MergeRule):
    pass


class _TestSelfModRule(BaseSelfModifyingRule):
    def __init__(self):
        pass


class _TestNonCasterRule(CompoundRule):
    def __init__(self):
        pass


class TestRuleFamilyValidator(TestCase):

    def setUp(self):
        self._validator = RuleFamilyValidator()
        self._rd_ccr_sm = RuleDetails(ccrtype=CCRType.SELFMOD)
        self._rd_nonccr = RuleDetails(name="some rule")
        self._rd_ccr_global = RuleDetails(ccrtype=CCRType.GLOBAL)
        self._rd_ccr_app = RuleDetails(ccrtype=CCRType.APP)

    def test_selfmod_passes_with_ccrtype_optional(self):
        self.assertIsNone(self._validator.validate(_TestSelfModRule(), self._rd_ccr_sm))
        self.assertIsNone(self._validator.validate(_TestSelfModRule(), self._rd_nonccr))

    def test_selfmod_ccr_fails_without_selfmod_ccr_type(self):
        self.assertIsNotNone(self._validator.validate(_TestSelfModRule(), self._rd_ccr_global))
        self.assertIsNotNone(self._validator.validate(_TestSelfModRule(), self._rd_ccr_app))

    def test_mergerule_passes_with_allowed_ccrtypes_only(self):
        self.assertIsNone(self._validator.validate(_TestMergeRule(), self._rd_ccr_global))
        self.assertIsNone(self._validator.validate(_TestMergeRule(), self._rd_ccr_app))
        self.assertIsNotNone(self._validator.validate(_TestMergeRule(), self._rd_ccr_sm))

    def test_mergerule_fails_without_ccrtype(self):
        self.assertIsNotNone(self._validator.validate(_TestMergeRule(), self._rd_nonccr))

    def test_non_mapping_rules_fail(self):
        self.assertIsNotNone(self._validator.validate(_TestNonCasterRule(), self._rd_nonccr))
        self.assertIsNotNone(self._validator.validate(_TestNonCasterRule(), self._rd_ccr_global))
        self.assertIsNotNone(self._validator.validate(_TestNonCasterRule(), self._rd_ccr_app))
        self.assertIsNotNone(self._validator.validate(_TestNonCasterRule(), self._rd_ccr_sm))

    def test_mapping_rule_passes_without_ccrtype(self):
        self.assertIsNone(self._validator.validate(_TestMappingRule(), self._rd_nonccr))

    def test_mapping_rule_fails_with_ccrtype(self):
        self.assertIsNotNone(self._validator.validate(_TestMappingRule(), self._rd_ccr_global))
        self.assertIsNotNone(self._validator.validate(_TestMappingRule(), self._rd_ccr_app))
        self.assertIsNotNone(self._validator.validate(_TestMappingRule(), self._rd_ccr_sm))
