from dragonfly import Key, Dictation

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class KDiff3Rule(MergeRule):
    pronunciation = "K diff"

    mapping = {
        "refresh": R(Key("f5")),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1, "mim": ""}


def get_rule():
    return KDiff3Rule, RuleDetails(executable="kdiff3")
