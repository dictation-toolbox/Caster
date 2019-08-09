from dragonfly import Mouse, Key, Repeat, Dictation

from castervoice.lib.actions import Text
from castervoice.lib.ctrl.mgr import rdcommon
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class NPPRule(MergeRule):
    pronunciation = "notepad plus plus"

    mapping = {
        "stylize <n2>":
            R(Mouse("right") + Key("down:6/5, right") +
              (Key("down")*Repeat(extra="n2")) + Key("enter")),
        "remove style":
            R(Mouse("right") + Key("down:6/5, right/5, down:5/5, enter")),
        "preview in browser":
            R(Key("cas-r")),

        # requires function list plug-in:
        "function list":
            R(Key("cas-l")),
        "open":
            R(Key("c-o")),
        "go [to] line <n>":
            R(Key("c-g/10") + Text("%(n)s") + Key("enter")),
    }
    extras = [
        Dictation("text"),
        IntegerRefST("n", 1, 1000),
        IntegerRefST("n2", 1, 10),
    ]
    defaults = {"n": 1}


def get_rule():
    return NPPRule, rdcommon.app_executable("notepad++")
