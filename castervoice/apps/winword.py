from dragonfly import Key, Dictation

from castervoice.lib.ctrl.mgr import rdcommon
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class MSWordRule(MergeRule):
    pronunciation = "Microsoft Word"

    mapping = {
        "insert image": R(Key("alt, n, p")),
    }
    extras = [
        Dictation("dict"),
        IntegerRefST("n", 1, 100),
    ]
    defaults = {"n": 1, "dict": "nothing"}


def get_rule():
    return MSWordRule, rdcommon.app_executable("winword")
