from unittest import TestCase

from dragonfly import MappingRule, Dictation, Choice

from castervoice.rules.core.alphabet_rules.alphabet import Alphabet
from castervoice.rules.core.navigation_rules.nav import Navigation
from castervoice.lib.merge.ccrmerging2.transformers.text_replacer.text_replacer import TextReplacerTransformer
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.actions2 import NullAction
from tests.lib.merge.ccrmerging2.transformers.text_replacer import mock_TRParser


class _TestMappingRule(MappingRule):

    mapping = {
        "some <text>": NullAction(),
        "other [<choice>]": NullAction()
    }

    extras = [
        Dictation("text"),
        Choice("choice", {
            "alarm": "alarm",
            "custom grid": "CustomGrid",
            "element": "e"
        }),
    ]
    defaults = {
        "text": "asdf"
    }


class _TestMergeRule(MergeRule):

    pronunciation = "test merge rule"

    mapping = {
        "some <text>": NullAction(),
        "other [<choice>]": NullAction()
    }

    extras = [
        Dictation("text"),
        Choice("choice", {
            "alarm": "alarm",
            "custom grid": "CustomGrid",
            "element": "e"
        }),
    ]
    defaults = {
        "text": "asdf"
    }


class TestTextReplacerTransformer(TestCase):

    def test_replace_mappingrule_spec(self):
        trt = TextReplacerTransformer(mock_TRParser.MockTRParser)
        rule = _TestMappingRule()
        mock_TRParser.MOCK_SPECS["some"] = "any"
        transformed_rule = trt.get_transformed_rule(rule)

        self.assertTrue("any <text>" in transformed_rule._mapping.keys())

    def test_replace_mergerule_spec(self):
        trt = TextReplacerTransformer(mock_TRParser.MockTRParser)
        rule = _TestMergeRule()
        mock_TRParser.MOCK_SPECS["some"] = "a few"
        transformed_rule = trt.get_transformed_rule(rule)

        self.assertTrue("a few <text>" in transformed_rule._mapping.keys())

    def test_replace_mergerule_extra(self):
        trt = TextReplacerTransformer(mock_TRParser.MockTRParser)
        rule = _TestMergeRule()
        mock_TRParser.MOCK_EXTRAS["element"] = "ornament"
        transformed_rule = trt.get_transformed_rule(rule)

        self.assertTrue("ornament" in transformed_rule._extras["choice"]._choices)
        self.assertEqual("e", transformed_rule._extras["choice"]._choices["ornament"])

    def test_replace_real_mergerule_extra(self):
        trt = TextReplacerTransformer(mock_TRParser.MockTRParser)
        rule = Alphabet()
        mock_TRParser.MOCK_EXTRAS["goof"] = "gas"
        transformed_rule = trt.get_transformed_rule(rule)

        self.assertTrue("gas" in transformed_rule._extras["letter"]._choices)
        self.assertEqual("g", transformed_rule._extras["letter"]._choices["gas"])

    def test_replace_real_mergerule_spec(self):
        trt = TextReplacerTransformer(mock_TRParser.MockTRParser)
        rule = Navigation()
        mock_TRParser.MOCK_SPECS["cut"] = "but"
        transformed_rule = trt.get_transformed_rule(rule)

        self.assertTrue("but [<nnavi500>]" in transformed_rule._mapping)

    def test_that_transformer_does_not_change_class_name(self):
        trt = TextReplacerTransformer(mock_TRParser.MockTRParser)
        mock_TRParser.MOCK_SPECS["some"] = "any"

        rule1 = _TestMappingRule()
        rule2 = _TestMergeRule()

        transformed_rule1 = trt.get_transformed_rule(rule1)
        self.assertEqual("_TestMappingRule", transformed_rule1.__class__.__name__)
        transformed_rule2 = trt.get_transformed_rule(rule2)
        self.assertEqual("_TestMergeRule", transformed_rule2.__class__.__name__)
