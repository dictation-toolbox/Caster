from dragonfly import Function, Choice

from caster.lib import navigation
from caster.lib.dfplus.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


class AlphabetCCR(MergeRule):
    mapping = {
        "[<big>] <letter>": R(Function(navigation.letters2, extra ={"big", "letter"}), rdescript="Spell"),
        }
    extras = [
        navigation.get_alphabet_choice("letter"),
        Choice("big",
              {"big": "big",
               }),
    ]
    defaults = {
    "big": "", 
    }