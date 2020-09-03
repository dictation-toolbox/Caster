from dragonfly import Repeat, Dictation, MappingRule


from castervoice.lib.actions import Key, Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.short import R


class VisualStudioRule(MappingRule):
    mapping = {
        "next tab [<n>]":
            R(Key("ca-pgdown"))*Repeat(extra="n"),
        "prior tab [<n>]":
            R(Key("ca-pgup"))*Repeat(extra="n"),
        "close tab [<n>]":
            R(Key("c-f4/20"))*Repeat(extra="n"),
        "(list | show) documents":
            R(Key("a-w, w")),
        "[focus] document (window | pane)":
            R(Key("a-w, w, enter")),
        "solution explorer":
            R(Key("ca-l")),
        "team explorer":
            R(Key("c-backslash, c-m")),
        "source control explorer":
            R(Key("c-q") + Text("Source Control Explorer") + Key("enter")),
        "quick launch":
            R(Key("c-q")),
        "go to line":
            R(Key("c-g")),
        "comment line":
            R(Key("c-k, c-c")),
        "comment block":
            R(Key("c-k, c-c")),
        "(un | on) comment line":
            R(Key("c-k/50, c-u")),
        "(un | on) comment block":
            R(Key("c-k/50, c-u")),
        "[toggle] full screen":
            R(Key("sa-enter")),
        "(set | toggle) bookmark":
            R(Key("c-k, c-k")),
        "next bookmark":
            R(Key("c-k, c-n")),
        "prior bookmark":
            R(Key("c-k, c-p")),
        "collapse to definitions":
            R(Key("c-m, c-o")),
        "toggle [section] outlining":
            R(Key("c-m, c-m")),
        "toggle all outlining":
            R(Key("c-m, c-l")),
        "[toggle] break point":
            R(Key("f9")),
        "step over [<n>]":
            R(Key("f10/50")*Repeat(extra="n")),
        "step into":
            R(Key("f11")),
        "step out [of]":
            R(Key("s-f11")),
        "(resume | go debug)":
            R(Key("f5")),
        "run tests":
            R(Key("c-r, t")),
        "run all tests":
            R(Key("c-r, a")),
        "build solution":
            R(Key("cs-b")),
        "get latest [version]":
            R(Key("a-f, r, l")),
        "(show | view) history":
            R(Key("a-f, r, h")),
        "compare (files | versions)":
            R(Key("a-f, r, h")),
        "undo (checkout | pending changes)":
            R(Key("a-f, r, u")),
        "[open] [go to] work item":
            R(Key("a-m, g")),
        "[add] [new] linked work item":
            R(Key("sa-l")),
        "go back":
            R(Key("c--")),
        "go forward":
            R(Key("cs--")),
        "go to definition":
            R(Key("f12")),
        "show refs":
            R(Key("a-2")),	
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1, "mim": ""}


def get_rule():
    return VisualStudioRule, RuleDetails(name="visual studio", executable="devenv")
