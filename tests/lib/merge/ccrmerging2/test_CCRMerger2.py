from itertools import permutations

from dragonfly.grammar.context import LogicNotContext, Context, LogicAndContext,FuncContext
from mock import Mock
from castervoice.lib.context import AppContext
from castervoice.rules.apps.editor.eclipse_rules.eclipse import EclipseCCR
from castervoice.rules.apps.editor.vscode_rules.vscode import VSCodeCcrRule
from castervoice.rules.core.alphabet_rules.alphabet import Alphabet
from castervoice.rules.core.navigation_rules.nav import Navigation
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.managed_rule import ManagedRule
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.ctrl.nexus import Nexus
from castervoice.lib.merge.ccrmerging2.sorting.config_ruleset_sorter import ConfigBasedRuleSetSorter
from castervoice.lib.merge.ccrmerging2.transformers.text_replacer.text_replacer import TextReplacerTransformer
from castervoice.lib.merge.ccrmerging2.transformers.transformers_runner import TransformersRunner
from tests.lib.merge.ccrmerging2.fake_rules import FakeRuleOne, FakeRuleTwo
from tests.lib.merge.ccrmerging2.transformers.text_replacer import mock_TRParser
from tests.test_util.settings_mocking import SettingsEnabledTestCase


class TestCCRMerger2(SettingsEnabledTestCase):

    @staticmethod
    def _create_managed_rule(rule_class, ccrtype, executable=None,function = None):
        return ManagedRule(rule_class, RuleDetails(ccrtype=ccrtype, executable=executable,function_context = function))

    def setUp(self):
        self._set_setting(["miscellaneous", "max_ccr_repetitions"], "4")
        self.selfmodrule_configurer = Mock()
        self.transformers_config = Mock()
        self.sorter = ConfigBasedRuleSetSorter(["Alphabet", "Navigation", "EclipseCCR", "VSCodeCcrRule"])
        self.transformers_runner = TransformersRunner(self.transformers_config)
        self.merger = Nexus._create_merger(self.selfmodrule_configurer, self.transformers_runner)

    def _extract_merged_rule_from_repeatrule(self, repeat_rule, index=0):
        return repeat_rule[index][0]._extras["caster_base_sequence"]._child._children[0]._rule

    def test_merge_empty(self):
        """
        Merger should run through empty list without errors.
        """
        self.merger.merge_rules([], self.sorter)

    def test_merge_nonempty(self):
        """
        Merger successfully "merge" one CCR rule w/ no context.
        """
        navigation_mr = TestCCRMerger2._create_managed_rule(Navigation, CCRType.GLOBAL)
        result = self.merger.merge_rules([navigation_mr], self.sorter)

        self.assertEqual(1, len(result.ccr_rules_and_contexts))
        repeat_rule = result.ccr_rules_and_contexts[0][0]
        context = result.ccr_rules_and_contexts[0][1]
        self.assertEqual("RepeatRule", repeat_rule.__class__.__name__)
        self.assertIsInstance(context, FuncContext)

    def test_merge_two(self):
        """
        Merger successfully merges two CCR rules w/ no context.
        """
        alphabet_mr = TestCCRMerger2._create_managed_rule(Alphabet, CCRType.GLOBAL)
        navigation_mr = TestCCRMerger2._create_managed_rule(Navigation, CCRType.GLOBAL)
        result = self.merger.merge_rules([alphabet_mr, navigation_mr], self.sorter)

        self.assertEqual(1, len(result.ccr_rules_and_contexts))
        repeat_rule = result.ccr_rules_and_contexts[0][0]
        context = result.ccr_rules_and_contexts[0][1]
        self.assertEqual("RepeatRule", repeat_rule.__class__.__name__)
        self.assertIsInstance(context, FuncContext)

    def test_merge_two_incompatible(self):
        """
        Merger KOs the earlier incompatible rule and leaves the later one.
        """
        sorter = ConfigBasedRuleSetSorter(["FakeRuleOne", "FakeRuleTwo"])
        self.merger = Nexus._create_merger(self.selfmodrule_configurer, self.transformers_runner)

        java_mr = TestCCRMerger2._create_managed_rule(FakeRuleOne, CCRType.GLOBAL)
        python_mr = TestCCRMerger2._create_managed_rule(FakeRuleTwo, CCRType.GLOBAL)
        result = self.merger.merge_rules([java_mr, python_mr], sorter)

        rule = self._extract_merged_rule_from_repeatrule(result.ccr_rules_and_contexts)
        self.assertIn("two exclusive", rule._mapping)
        self.assertNotIn("one exclusive", rule._mapping)

    def test_merge_one_context_one_no_context(self):
        """
        One contexted CCR rule and one non-contexted mergerule should result in two
        RepeatRules, the contexted one with a Context aligned with it and the non-contexted
        one with a LogicNotContext aligned with it.
        """
        eclipse_mr = TestCCRMerger2._create_managed_rule(EclipseCCR, CCRType.APP, "eclipse")
        navigation_mr = TestCCRMerger2._create_managed_rule(Navigation, CCRType.GLOBAL)
        result = self.merger.merge_rules([eclipse_mr, navigation_mr], self.sorter)

        self.assertEqual(2, len(result.ccr_rules_and_contexts))
        self.assertEqual("RepeatRule", result.ccr_rules_and_contexts[0][0].__class__.__name__)
        self.assertEqual("RepeatRule", result.ccr_rules_and_contexts[1][0].__class__.__name__)
        self.assertIsInstance(result.ccr_rules_and_contexts[0][1], FuncContext)
        self.assertIsInstance(result.ccr_rules_and_contexts[1][1], Context)

    def test_words_txt_transformer(self):
        """
        Merger should use TextReplacerTransformer to replace "clear" with "bear" in specs
        and "goof" with "gas" in extras.
        """
        # transformer setup
        self.transformers_config.is_transformer_active.side_effect = [True, True]
        trt = TextReplacerTransformer(mock_TRParser.MockTRParser)
        mock_TRParser.MOCK_SPECS["clear"] = "bear"
        mock_TRParser.MOCK_EXTRAS["goof"] = "gas"
        self.transformers_runner._transformers.append(trt)

        # rule setup
        alphabet_mr = TestCCRMerger2._create_managed_rule(Alphabet, CCRType.GLOBAL)
        navigation_mr = TestCCRMerger2._create_managed_rule(Navigation, CCRType.GLOBAL)
        result = self.merger.merge_rules([alphabet_mr, navigation_mr], self.sorter)

        self.assertEqual(1, len(result.ccr_rules_and_contexts))

        rule = self._extract_merged_rule_from_repeatrule(result.ccr_rules_and_contexts)
        self.assertTrue("bear [<nnavi50>]" in rule._mapping.keys())
        self.assertTrue("gas" in rule._extras["letter"]._choices)

    def test_merge_two_app_ccr(self):
        """
        Merger successfully merges one global + two CCR app rules.
        """
        alphabet_mr = TestCCRMerger2._create_managed_rule(Alphabet, CCRType.GLOBAL)
        eclipse_app_mr = TestCCRMerger2._create_managed_rule(EclipseCCR, CCRType.APP, "eclipse")
        vscode_app_mr = TestCCRMerger2._create_managed_rule(VSCodeCcrRule, CCRType.APP, "vscode")
        result = self.merger.merge_rules([alphabet_mr, eclipse_app_mr, vscode_app_mr], self.sorter)

        self.assertEqual(3, len(result.ccr_rules_and_contexts))
        repeat_rule_1, context_1 = result.ccr_rules_and_contexts[0]
        repeat_rule_2, context_2 = result.ccr_rules_and_contexts[1]
        repeat_rule_3, context_3 = result.ccr_rules_and_contexts[2]
        self.assertEqual("RepeatRule", repeat_rule_1.__class__.__name__)
        self.assertEqual("RepeatRule", repeat_rule_2.__class__.__name__)
        self.assertEqual("RepeatRule", repeat_rule_3.__class__.__name__)
        self.assertIsInstance(context_1, FuncContext)
        self.assertIsInstance(context_2, AppContext)
        self.assertIsInstance(context_3, AppContext)
        # TODO: write a similar unit test to check the executables/titles validity of the contexts produced
