from dragonfly import Pause, Function, Choice, MappingRule, ShortIntegerRef

from castervoice.lib.actions import Key, Text, Mouse

from castervoice.lib import navigation
from castervoice.lib.actions import Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R
from castervoice.lib.temporary import Store, Retrieve


class RStudioRule(MappingRule):
    mapping = {
    "new file":
        R(Key("cs-n")),
    "open file":
        R(Key("c-o")),
    "open recent project":
        R(Key("a-f, j")),
  	"open project":
        R(Key("a-f, n, enter")),
    "save all":
        R(Key("ac-s")),
    "select all":
        R(Key("c-a")),
    "find":
        R(Key("c-f")),

    "[go to] line <ln1>":
        R(Key("as-g") + Pause("10") + Text("%(ln1)s") + Key("enter")),
    "<action> [line] <ln1> [by <ln2>]"  :
        R(Function(navigation.action_lines, go_to_line="as-g/10", select_line_down="s-down", wait="/3", upon_arrival="home, ")),

    "focus console":
        R(Key("c-2")),
    "focus main":
        R(Key("c-1")),

    "next tab":
        R(Key("c-f12")),
    "first tab":
        R(Key("cs-f11")),
    "previous tab":
        R(Key("c-f11")),
    "last tab":
        R(Key("cs-f12")),
    "close tab":
        R(Key("c-w")),


    "run line":
        R(Key("c-enter")),
    "run document":
        R(Key("ac-r")),
    "comment (line | selected)":
        R(Key("cs-c")),

    "next plot":
        R(Key("ac-f12")),
    "previous plot":
        R(Key("ac-f11")),

    "(help | document) that":
        R(Store() + Key("c-2, question") + Retrieve() + Key("enter, c-3")),
    "glimpse that":
        R(Store() + Key("c-2") + Retrieve() + Key("space, percent, rangle, percent") + Text(" glimpse()") + Key("enter/50, c-1")),
    "vee table that":
        R(Store() + Key("c-2") + Text("library(vtable)") + Key("enter/50") + Retrieve() + Key("space, percent, rangle, percent") + Text(" vtable()") + Key("enter/50, c-1")),

    }
    extras = [
        ShortIntegerRef("ln1", 1, 10000),
        ShortIntegerRef("ln2", 1, 10000),
        Choice("action", navigation.actions),
    ]
    defaults = {"ln2": ""}


def get_rule():
    details = RuleDetails(name="are studio", executable="rstudio")
    return RStudioRule, details
