from dragonfly import Function, Choice


try:  # Try first loading from caster user directory
    import alphabet_support
except ImportError:
    from castervoice.rules.core.alphabet_rules import alphabet_support

from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class Alphabet(MergeRule):
    pronunciation = "alphabet"

    mapping = {
        "[<big>] <letter>":
            R(Function(alphabet_support.letters2, extra={"big", "letter"})),
    }
    extras = [
        alphabet_support.get_alphabet_choice("letter"),
        Choice("big", {
            "big": True,
        }),
    ]
    defaults = {
        "big": False,
    }


def get_rule():
    return Alphabet, RuleDetails(ccrtype=CCRType.GLOBAL)
