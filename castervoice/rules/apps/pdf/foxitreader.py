from dragonfly import Repeat, Dictation, MappingRule, ShortIntegerRef

from castervoice.lib.actions import Key

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class FoxitRule(MappingRule):
    mapping = {
        "next tab [<n>]": R(Key("c-tab"))*Repeat(extra="n"),
        "prior tab [<n>]": R(Key("cs-tab"))*Repeat(extra="n"),
        "close tab [<n>]": R(Key("c-f4/20"))*Repeat(extra="n"),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        ShortIntegerRef("n", 1, 1000),
    ]
    defaults = {"n": 1, "mim": ""}


def get_rule():
    return FoxitRule, RuleDetails(name="fox it reader", title="Foxit Reader")
