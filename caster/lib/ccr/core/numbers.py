from dragonfly import Text, Choice

from caster.lib import control, alphanumeric
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge.ccrmerger import CCRMerger
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


class Numbers(MergeRule):
    pronunciation = CCRMerger.CORE[2]
    mapping = {
        "word number <wn>":
            R(Text("%(wn)s"), rdescript="Number As Word"),
        "numb <wnKK>":
            R(Text("%(wnKK)s"),
              rspec="number", rdescript="Number"),
    }

    extras = [
        Choice("wn", {
            "zero": "zero",
            "one": "one",
            "two": "two",
            "three": "three",
            "four": "four",
            "five": "five",
            "six": "six",
            "seven": "seven",
            "eight": "eight",
            "nine": "nine",
    }),
        IntegerRefST("wnKK", 0, 1000000),
    ]
    defaults = {}


control.nexus().merger.add_global_rule(Numbers())
