from castervoice.lib.imports import *

class Alphabet(MergeRule):
    pronunciation = CCRMerger.CORE[0]

    mapping = {
        "[<big>] <letter>":
            R(Function(alphanumeric.letters2, extra={"big", "letter"}),
              rdescript="Core: Spell"),
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


control.nexus().merger.add_global_rule(Alphabet())
