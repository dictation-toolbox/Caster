from unittest import TestCase

from dragonfly import MappingRule, Dictation, Choice

from castervoice.lib.ccr.core.alphabet import Alphabet
from castervoice.lib.merge.ccrmerging2.transformers.text_replacer.text_replacer import TextReplacerTransformer
from castervoice.lib.merge.ccrmerging2.transformers.text_replacer.tr_definitions import TRDefinitions
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.actions2 import NullAction

_MOCK_SPECS = {}
_MOCK_EXTRAS = {}
_MOCK_DEFAULTS = {}


class _MockTRParser(object):

    def create_definitions(self):
        return TRDefinitions(_MOCK_SPECS, _MOCK_EXTRAS, _MOCK_DEFAULTS)


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
        trt = TextReplacerTransformer(_MockTRParser)
        rule = _TestMappingRule()
        _MOCK_SPECS["some"] = "any"
        transformed_rule = trt.get_transformed_rule(rule)

        self.assertTrue("any <text>" in transformed_rule._mapping.keys())

    def test_replace_mergerule_spec(self):
        trt = TextReplacerTransformer(_MockTRParser)
        rule = _TestMergeRule()
        _MOCK_SPECS["some"] = "a few"
        transformed_rule = trt.get_transformed_rule(rule)

        self.assertTrue("a few <text>" in transformed_rule._mapping.keys())

    def test_replace_mergerule_extra(self):
        trt = TextReplacerTransformer(_MockTRParser)
        rule = _TestMergeRule()
        _MOCK_EXTRAS["element"] = "ornament"
        transformed_rule = trt.get_transformed_rule(rule)

        self.assertTrue("ornament" in transformed_rule._extras["choice"]._choices)
        self.assertEqual("e", transformed_rule._extras["choice"]._choices["ornament"])

    def test_replace_real_mergerule_extra(self):
        trt = TextReplacerTransformer(_MockTRParser)
        rule = Alphabet()
        _MOCK_EXTRAS["goof"] = "gas"
        transformed_rule = trt.get_transformed_rule(rule)

        self.assertTrue("gas" in transformed_rule._extras["letter"]._choices)
        self.assertEqual("g", transformed_rule._extras["letter"]._choices["gas"])

    def test_that_transformer_does_not_change_class_name(self):
        trt = TextReplacerTransformer(_MockTRParser)
        _MOCK_SPECS["some"] = "any"

        rule1 = _TestMappingRule()
        rule2 = _TestMergeRule()

        transformed_rule1 = trt.get_transformed_rule(rule1)
        self.assertEqual("_TestMappingRule", transformed_rule1.__class__.__name__)
        transformed_rule2 = trt.get_transformed_rule(rule2)
        self.assertEqual("_TestMergeRule", transformed_rule2.__class__.__name__)
