from dragonfly import Function

from castervoice.lib import const, alphanumeric
from castervoice.lib.ctrl.mgr import rdcommon
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class Numbers(MergeRule):
    pronunciation = const.CORE[2]
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
    return Numbers, rdcommon.ccr_global()
