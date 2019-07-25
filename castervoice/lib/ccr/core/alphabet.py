from castervoice.lib import const
from castervoice.lib.imports import *


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

control.global_rule(Alphabet())
