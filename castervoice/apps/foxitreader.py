from dragonfly import Key, Repeat, Dictation

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class FoxitRule(MergeRule):
    pronunciation = "fox it reader"

    mapping = {
        "next tab [<n>]": R(Key("c-tab"))*Repeat(extra="n"),
        "prior tab [<n>]": R(Key("cs-tab"))*Repeat(extra="n"),
        "close tab [<n>]": R(Key("c-f4/20"))*Repeat(extra="n"),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1, "mim": ""}


def get_rule():
    return FoxitRule, RuleDetails(title="Foxit Reader")
