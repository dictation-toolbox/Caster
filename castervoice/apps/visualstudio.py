from dragonfly import (Grammar, Dictation, Repeat)

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R
from castervoice.lib.context import AppContext
from castervoice.lib.actions import (Key, Text)


class VisualStudioRule(MergeRule):
    pronunciation = "visual studio"

    mapping = {
        "next tab [<n>]":
            R(Key("ca-pgdown"), rdescript="Visual Studio: Next Tab")*Repeat(extra="n"),
        "prior tab [<n>]":
            R(Key("ca-pgup"), rdescript="Visual Studio: Previous Tab")*Repeat(extra="n"),
        "close tab [<n>]":
            R(Key("c-f4/20"), rdescript="Visual Studio: Close Tab")*Repeat(extra="n"),
        "(list | show) documents":
            R(Key("a-w, w"), rdescript="Visual Studio: List Documents"),
        "[focus] document (window | pane)":
            R(Key("a-w, w, enter"), rdescript="Visual Studio: Focus Document Pane"),
        "solution explorer":
            R(Key("ca-l"), rdescript="Visual Studio: Solution Explorer"),
        "team explorer":
            R(Key("c-backslash, c-m"), rdescript="Visual Studio: Team Explorer"),
        "source control explorer":
            R(Key("c-q") + Text("Source Control Explorer") + Key("enter"),
              rdescript="Visual Studio: Source Control Explorer"),
        "quick launch":
            R(Key("c-q"), rdescript="Visual Studio: Quick Launch"),
        "go to line":
            R(Key("c-g"), rdescript="Visual Studio: Go To Line"),
        "comment line":
            R(Key("c-k, c-c"), rdescript="Visual Studio: Comment Selection"),
        "comment block":
            R(Key("c-k, c-c"), rdescript="Visual Studio: Comment Block"),
        "(un | on) comment line":
            R(Key("c-k/50, c-u"), rdescript="Visual Studio: Uncomment Selection"),
        "(un | on) comment block":
            R(Key("c-k/50, c-u"), rdescript="Visual Studio: Uncomment Block"),
        "[toggle] full screen":
            R(Key("sa-enter"), rdescript="Visual Studio: Fullscreen"),
        "(set | toggle) bookmark":
            R(Key("c-k, c-k"), rdescript="Visual Studio: Toggle Bookmark"),
        "next bookmark":
            R(Key("c-k, c-n"), rdescript="Visual Studio: Next Bookmark"),
        "prior bookmark":
            R(Key("c-k, c-p"), rdescript="Visual Studio: Previous Bookmark"),
        "collapse to definitions":
            R(Key("c-m, c-o"), rdescript="Visual Studio: Collapse To Definitions"),
        "toggle [section] outlining":
            R(Key("c-m, c-m"), rdescript="Visual Studio: Toggle Section Outlining"),
        "toggle all outlining":
            R(Key("c-m, c-l"), rdescript="Visual Studio: Toggle All Outlining"),
        "[toggle] breakpoint":
            R(Key("f9"), rdescript="Visual Studio: Breakpoint"),
        "step over [<n>]":
            R(Key("f10/50")*Repeat(extra="n"), rdescript="Visual Studio: Step Over"),
        "step into":
            R(Key("f11"), rdescript="Visual Studio: Step Into"),
        "step out [of]":
            R(Key("s-f11"), rdescript="Visual Studio: Step Out"),
        "resume":
            R(Key("f5"), rdescript="Visual Studio: Resume"),
        "run tests":
            R(Key("c-r, t"), rdescript="Visual Studio: Run test(s)"),
        "run all tests":
            R(Key("c-r, a"), rdescript="Visual Studio: Run all tests"),
        "build solution":
            R(Key("cs-b"), rdescript="Visual Studio: Build solution"),
        "get latest [version]":
            R(Key("a-f, r, l"), rdescript="Visual Studio: Get Latest"),
        "(show | view) history":
            R(Key("a-f, r, h"), rdescript="Visual Studio: Show History"),
        "compare (files | versions)":
            R(Key("a-f, r, h"), rdescript="Visual Studio: Compare..."),
        "undo (checkout | pending changes)":
            R(Key("a-f, r, u"), rdescript="Visual Studio: Undo Pending Changes"),
        "[open] [go to] work item":
            R(Key("a-m, g"), rdescript="Visual Studio: Open Work Item"),
        "[add] [new] linked work item":
            R(Key("sa-l"), rdescript="Visual Studio: New Linked Work Item"),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1, "mim": ""}


#---------------------------------------------------------------------------

context = AppContext(executable="devenv")
grammar = Grammar("Visual Studio", context=context)

if settings.SETTINGS["apps"]["visualstudio"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(VisualStudioRule())
    else:
        rule = VisualStudioRule(name="visualstudio")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
