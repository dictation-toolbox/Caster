from unittest import TestCase

from dragonfly import MappingRule, Dictation, Choice

from castervoice.rules.core.alphabet_rules.alphabet import Alphabet
from castervoice.rules.core.navigation_rules.nav import Navigation
from castervoice.lib.merge.ccrmerging2.transformers.text_replacer.text_replacer import TextReplacerTransformer
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.actions2 import NullAction
from tests.lib.merge.ccrmerging2.transformers.text_replacer.mock_TRParser import MockTRParser


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


def _create_mock_parser(specs={}, extras={}, defaults={}):
    return lambda: MockTRParser(specs, extras, defaults)


class TestTextReplacerTransformer(TestCase):

    def test_replace_mappingrule_spec(self):
        parser_fn = _create_mock_parser(specs={"some": "any"})
        trt = TextReplacerTransformer(parser_fn)
        rule = _TestMappingRule()
        transformed_rule = trt.get_transformed_rule(rule)

        self.assertTrue("any <text>" in transformed_rule._mapping.keys())

    def test_replace_mergerule_spec(self):
        parser_fn = _create_mock_parser(specs={"some": "a few"})
        trt = TextReplacerTransformer(parser_fn)
        rule = _TestMergeRule()
        transformed_rule = trt.get_transformed_rule(rule)

        self.assertTrue("a few <text>" in transformed_rule._mapping.keys())

    def test_replace_mergerule_extra(self):
        parser_fn = _create_mock_parser(extras={"element": "ornament"})
        trt = TextReplacerTransformer(parser_fn)
        rule = _TestMergeRule()
        transformed_rule = trt.get_transformed_rule(rule)

        self.assertTrue("ornament" in transformed_rule._extras["choice"]._choices)
        self.assertEqual("e", transformed_rule._extras["choice"]._choices["ornament"])

    def test_replace_real_mergerule_extra(self):
        parser_fn = _create_mock_parser(extras={"goof": "gas"})
        trt = TextReplacerTransformer(parser_fn)
        rule = Alphabet()
        transformed_rule = trt.get_transformed_rule(rule)

        self.assertTrue("gas" in transformed_rule._extras["letter"]._choices)
        self.assertEqual("g", transformed_rule._extras["letter"]._choices["gas"])

    def test_replace_real_mergerule_spec(self):
        parser_fn = _create_mock_parser(specs={"cut": "but"})
        trt = TextReplacerTransformer(parser_fn)
        rule = Navigation()
        transformed_rule = trt.get_transformed_rule(rule)

        self.assertTrue("but [<nnavi500>]" in transformed_rule._mapping)

    def test_that_transformer_does_not_change_class_name(self):
        parser_fn = _create_mock_parser(specs={"some": "any"})
        trt = TextReplacerTransformer(parser_fn)

        rule1 = _TestMappingRule()
        rule2 = _TestMergeRule()

        transformed_rule1 = trt.get_transformed_rule(rule1)
        self.assertEqual("_TestMappingRule", transformed_rule1.__class__.__name__)
        transformed_rule2 = trt.get_transformed_rule(rule2)
        self.assertEqual("_TestMergeRule", transformed_rule2.__class__.__name__)

    def test_move_required_extra(self):
        """
        The user should be allowed to move a required extra.
        """
        parser_fn = _create_mock_parser(specs={"some <text>": "<text> some"})
        trt = TextReplacerTransformer(parser_fn)
        rule = _TestMappingRule()
        transformed_rule = trt.get_transformed_rule(rule)

        self.assertTrue("<text> some" in transformed_rule._mapping.keys())

    def test_remove_optional_extra(self):
        """
        The user should be allowed to remove an optional extra.
        """
        parser_fn = _create_mock_parser(specs={"other [<choice>]": "just other"})
        trt = TextReplacerTransformer(parser_fn)
        rule = _TestMappingRule()
        transformed_rule = trt.get_transformed_rule(rule)

        self.assertTrue("just other" in transformed_rule._mapping.keys())

    def test_rename_required_extra(self):
        """
        The user should not be allowed to rename a required extra.
        """
        parser_fn = _create_mock_parser(specs={"some <text>": "some <thing>"})
        trt = TextReplacerTransformer(parser_fn)
        rule = _TestMappingRule()
        transformed_rule = trt.get_transformed_rule(rule)

        self.assertTrue("some <text>" in transformed_rule._mapping.keys())

    def test_remove_required_extra(self):
        """
        The user should not be allowed to remove a required extra.
        """
        parser_fn = _create_mock_parser(specs={"some <text>": "just some"})
        trt = TextReplacerTransformer(parser_fn)
        rule = _TestMappingRule()
        transformed_rule = trt.get_transformed_rule(rule)

        self.assertTrue("some <text>" in transformed_rule._mapping.keys())
