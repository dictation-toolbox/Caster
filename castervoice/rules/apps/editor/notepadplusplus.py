from dragonfly import Repeat, Dictation, MappingRule, ShortIntegerRef

from castervoice.lib.actions import Key, Text, Mouse

from castervoice.lib.actions import Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class NPPRule(MappingRule):

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
        ShortIntegerRef("n", 1, 1000),
        ShortIntegerRef("n2", 1, 10),
    ]
    defaults = {"n": 1}


def get_rule():
    return NPPRule, RuleDetails(name="notepad plus plus", executable="notepad++")
