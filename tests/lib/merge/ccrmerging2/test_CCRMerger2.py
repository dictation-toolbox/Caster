from dragonfly.grammar.context import LogicNotContext, Context, LogicAndContext
from mock import Mock
from castervoice.lib.context import AppContext
from castervoice.apps.eclipse import EclipseCCR
from castervoice.apps.vscode import VSCodeCcrRule
from castervoice.lib.ccr.core.alphabet import Alphabet
from castervoice.lib.ccr.core.nav import Navigation
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.managed_rule import ManagedRule
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.ctrl.nexus import Nexus
from castervoice.lib.merge.ccrmerging2.transformers.text_replacer.text_replacer import TextReplacerTransformer
from castervoice.lib.merge.ccrmerging2.transformers.transformers_runner import TransformersRunner
from tests.lib.merge.ccrmerging2.fake_rules import FakeRuleOne, FakeRuleTwo
from tests.lib.merge.ccrmerging2.transformers.text_replacer import mock_TRParser
from tests.test_util.settings_mocking import SettingsEnabledTestCase


class TestCCRMerger2(SettingsEnabledTestCase):

    @staticmethod
    def _create_managed_rule(rule_class, ccrtype, executable=None):
        return ManagedRule(rule_class, RuleDetails(ccrtype=ccrtype, executable=executable))

    def setUp(self):
        self._set_setting(["miscellaneous", "max_ccr_repetitions"], "4")
        order_fn = lambda: ["Alphabet", "Navigation", "EclipseCCR", "VSCodeCcrRule"]
        self.selfmodrule_configurer = Mock()
        self.transformers_config = Mock()
        self.transformers_runner = TransformersRunner(self.transformers_config)
        self.merger = Nexus._create_merger(order_fn, self.selfmodrule_configurer, self.transformers_runner)

    def _extract_merged_rule_from_repeatrule(self, repeat_rule, index=0):
        return repeat_rule[index][0]._extras["caster_base_sequence"]._child._children[0]._rule

    def test_merge_empty(self):
        """
        Merger should run through empty list without errors.
        """
        self.merger.merge([])

    def test_merge_nonempty(self):
        """
        Merger successfully "merge" one CCR rule w/ no context.
        """
        navigation_mr = TestCCRMerger2._create_managed_rule(Navigation, CCRType.GLOBAL)
        result = self.merger.merge([navigation_mr])

        self.assertEqual(1, len(result))
        repeat_rule = result[0][0]
        context = result[0][1]
        self.assertEqual("RepeatRule", repeat_rule.__class__.__name__)
        self.assertIsNone(context)

    def test_merge_two(self):
        """
        Merger successfully merges two CCR rules w/ no context.
        """
        alphabet_mr = TestCCRMerger2._create_managed_rule(Alphabet, CCRType.GLOBAL)
        navigation_mr = TestCCRMerger2._create_managed_rule(Navigation, CCRType.GLOBAL)
        result = self.merger.merge([alphabet_mr, navigation_mr])

        self.assertEqual(1, len(result))
        repeat_rule = result[0][0]
        context = result[0][1]
        self.assertEqual("RepeatRule", repeat_rule.__class__.__name__)
        self.assertIsNone(context)

    def test_merge_two_incompatible(self):
        """
        Merger KOs the earlier incompatible rule and leaves the later one.
        """
        order_fn = lambda: ["FakeRuleOne", "FakeRuleTwo"]
        self.merger = Nexus._create_merger(order_fn, self.selfmodrule_configurer, self.transformers_runner)

        java_mr = TestCCRMerger2._create_managed_rule(FakeRuleOne, CCRType.GLOBAL)
        python_mr = TestCCRMerger2._create_managed_rule(FakeRuleTwo, CCRType.GLOBAL)
        result = self.merger.merge([java_mr, python_mr])

        rule = self._extract_merged_rule_from_repeatrule(result)
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
        result = self.merger.merge([eclipse_mr, navigation_mr])

        self.assertEqual(2, len(result))
        self.assertEqual("RepeatRule", result[0][0].__class__.__name__)
        self.assertEqual("RepeatRule", result[1][0].__class__.__name__)
        self.assertIsInstance(result[0][1], LogicNotContext)
        self.assertIsInstance(result[1][1], Context)

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
        result = self.merger.merge([alphabet_mr, navigation_mr])

        self.assertEqual(1, len(result))

        rule = self._extract_merged_rule_from_repeatrule(result)
        self.assertTrue("bear [<nnavi50>]" in rule._mapping.keys())
        self.assertTrue("gas" in rule._extras["letter"]._choices)

    def test_merge_two_app_ccr(self):
        """
        Merger successfully merges one global + two CCR app rules.
        """
        alphabet_mr = TestCCRMerger2._create_managed_rule(Alphabet, CCRType.GLOBAL)
        eclipse_app_mr = TestCCRMerger2._create_managed_rule(EclipseCCR, CCRType.APP, "eclipse")
        vscode_app_mr = TestCCRMerger2._create_managed_rule(VSCodeCcrRule, CCRType.APP, "vscode")
        result = self.merger.merge([alphabet_mr, eclipse_app_mr, vscode_app_mr])

        self.assertEqual(3, len(result))
        repeat_rule_1, context_1 = result[0]
        repeat_rule_2, context_2 = result[1]
        repeat_rule_3, context_3 = result[2]
        self.assertEqual("RepeatRule", repeat_rule_1.__class__.__name__)
        self.assertEqual("RepeatRule", repeat_rule_2.__class__.__name__)
        self.assertEqual("RepeatRule", repeat_rule_3.__class__.__name__)
        self.assertIsInstance(context_1, LogicAndContext)
        self.assertIsInstance(context_2, AppContext)
        self.assertIsInstance(context_3, AppContext)
        # TODO: write a similar unit test to check the executables/titles validity of the contexts produced
