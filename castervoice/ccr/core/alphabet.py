from dragonfly import Function, Choice

from castervoice.lib import alphanumeric
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class Alphabet(MergeRule):
    pronunciation = "alphabet"

    mapping = {
        "[<big>] <letter>":
            R(Function(alphanumeric.letters2, extra={"big", "letter"})),
    }
    extras = [
        alphanumeric.get_alphabet_choice("letter"),
        Choice("big", {
            "big": True,
        }),
    ]
    defaults = {
        "big": False,
    }


def get_rule():
    return Alphabet, RuleDetails(ccrtype=CCRType.GLOBAL)
