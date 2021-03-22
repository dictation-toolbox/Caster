from dragonfly import Dictation, MappingRule, ShortIntegerRef
from castervoice.lib.actions import Key
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class KDiff3Rule(MappingRule):
    mapping = {
        "refresh": R(Key("f5")),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        ShortIntegerRef("n", 1, 1000),
    ]
    defaults = {"n": 1, "mim": ""}


def get_rule():
    return KDiff3Rule, RuleDetails(name="K diff", executable="kdiff3")
