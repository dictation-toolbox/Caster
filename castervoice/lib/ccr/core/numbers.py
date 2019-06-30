from castervoice.lib.imports import *

class Numbers(MergeRule):
    pronunciation = CCRMerger.CORE[2]
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


control.global_rule(Numbers())
