from dragonfly import Function

from castervoice.lib import alphanumeric
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class Numbers(MergeRule):
    pronunciation = "numbers"
    mapping = {
        "word number <wn>":
            R(Function(alphanumeric.word_number, extra="wn")),
        "numb <wnKK>":
            R(Function(alphanumeric.numbers2, extra="wnKK"),
              rspec="Number"),
    }

    extras = [
        IntegerRefST("wn", 0, 10),
        IntegerRefST("wnKK", 0, 1000000),
    ]
    defaults = {}


def get_rule():
    return Numbers, RuleDetails(ccrtype=CCRType.GLOBAL)
