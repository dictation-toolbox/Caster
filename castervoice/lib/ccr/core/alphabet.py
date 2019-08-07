from dragonfly import Function, Choice

from castervoice.lib import const, alphanumeric
from castervoice.lib.ctrl.mgr import rdcommon
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class Alphabet(MergeRule):
    pronunciation = const.CORE[0]

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
    return Alphabet, rdcommon.ccr_global()
