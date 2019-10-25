from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.actions2 import NullAction


class FakeRuleOne(MergeRule):
    mapping = {
        "a": NullAction(),
        "b": NullAction(),
        "one exclusive": NullAction()
    }


class FakeRuleTwo(MergeRule):
    mapping = {
        "a": NullAction(),
        "b": NullAction(),
        "two exclusive": NullAction()
    }


class FakeRuleThree(MergeRule):
    mapping = {
        "c": NullAction()
    }
