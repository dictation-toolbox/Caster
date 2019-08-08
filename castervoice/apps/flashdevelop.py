from dragonfly import Key, Dictation, Pause

from castervoice.lib.actions import Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class FlashDevelopCCR(MergeRule):
    pronunciation = "flash develop"

    mapping = {
        "[go to] line <n>": R(Key("c-g") + Pause("50") + Text("%(n)d") + Key("enter")),
    }
    extras = [
        Dictation("text"),
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1}


def get_rule():
    return FlashDevelopCCR, RuleDetails(executable="FlashDevelop", title="FlashDevelop")
