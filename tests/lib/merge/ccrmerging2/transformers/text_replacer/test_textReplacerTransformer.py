from unittest import TestCase

from dragonfly import MappingRule, Dictation, Choice

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
        self.assertEqual("_TestMappingRule", transformed_rule.__class__.__name__)

    def test_replace_mergerule_spec(self):
        trt = TextReplacerTransformer(_MockTRParser)
        rule = _TestMergeRule()
        _MOCK_SPECS["some"] = "a few"
        transformed_rule = trt.get_transformed_rule(rule)

        self.assertTrue("a few <text>" in transformed_rule._mapping.keys())
        self.assertEqual("_TestMergeRule", transformed_rule.__class__.__name__)
