from dragonfly import Choice, Function, ShortIntegerRef

try:  # Try first loading from caster user directory
    from numeric_support import word_number, numbers2
except ImportError: 
    from castervoice.rules.core.numbers_rules.numeric_support import word_number, numbers2
    
from castervoice.lib.actions import Text
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class Numbers(MergeRule):
    pronunciation = "numbers"
    mapping = {
        "word number <wn>":
            R(Function(word_number, extra="wn")),
        "[<long>] numb <wnKK>":
            R(Text("%(long)s") + Function(numbers2, extra="wnKK") + Text("%(long)s"),
              rspec="Number"),
    }

    extras = [
        ShortIntegerRef("wn", 0, 10),
        ShortIntegerRef("wnKK", 0, 1000000),
        Choice(
            "long", {
                "long": " ",
            }),
    ]

    defaults = {
        "long": "",
    }

def get_rule():
    return Numbers, RuleDetails(ccrtype=CCRType.GLOBAL)
