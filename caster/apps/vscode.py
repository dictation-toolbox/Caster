from dragonfly import (Grammar, Dictation, Repeat, Function)

from caster.lib import control
from caster.lib import settings
from caster.lib.actions import Key, Text
from caster.lib.context import AppContext
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


def findNthToken(text, n, direction):
    Key("c-f").execute()
    Text("%(text)s").execute({"text": text})
    if direction == "reverse":
        print("yeah? %(n)d")
        Key("s-enter:%(n)d").execute()
    else:
        Key("enter:%(n)d").execute()
        print("no? %(n)d")
    Key('escape').execute()


class VisualStudioCodeRule(MergeRule):
    pronunciation = "visual studio code"

    mapping = {
        ### ported from my dragonfly scripts
        # File management
        "[open] command palette":
            R(Key("cs-p"), rdescript="Visual Studio Code: Command Palette"),
        "(Open [file] | Go to [tab]) [<text>]":
            R(Key("c-p") + Text("%(text)s"), rdescript="Visual Studio Code: Go To File"),
        "Close tab":
            R(Key("c-w"), rdescript="Visual Studio Code: Close Tab"),
        "Save file":
            R(Key("c-s"), rdescript="Visual Studio Code: Save File"),
        "Save and close":
            R(Key("c-s/10, c-w"), rdescript="Visual Studio Code: Save And Close File"),

        # Search
        "(search | find in) [all] (files | codebase)":
            R(Key("cs-f"), rdescript="Visual Studio Code: Find in Codebase"),
        "(search | find) [file]":
            R(Key("c-f"), rdescript="Visual Studio Code: Find in File"),
        "(Find | Jump [to]) next <text>":
            R(Function(findNthToken, n=1, direction="forward"),
              rdescript="Visual Studio Code: Find Next"),
        "(Find | Jump [to]) previous <text>":
            R(Function(findNthToken, n=1, direction="reverse"),
              rdescript="Visual Studio Code: Find Previous"),

        # Tab management
        "nexta [<n>]":
            R(Key("c-pgdown"), rdescript="Visual Studio Code: Next Tab")*Repeat(
                extra="n"
            ),  # These would be next and previous tab but i have a conflict with chrome
        "prexta [<n>]":
            R(Key("c-pgup"), rdescript="Visual Studio Code: Previous Tab")*
            Repeat(extra="n"),
        "Close tab":
            R(Key("c-f4"), rdescript="Visual Studio Code: Close Tab"),
        "Exit preview":
            R(Key("space, c-z"), rdescript="Visual Studio Code: Exit Preview"),

        # moving around a file
        "(go to | jump | jump to) line <n>":
            R(Key("c-g") + Text("%(n)d") + Key("enter"),
              rdescript="Visual Studio Code: Go to Line"),
        "Go to definition":
            R(Key("f12"), rdescript="Visual Studio Code: Go to Definition"),
        "Go to required definition":
            R(Key("c-f12:2, c-right:5, left/50, f12"),
              rdescript="Visual Studio Code: Go to Required Definition"),
        "Go to (top | first line)":
            R(Key("c-home"), rdescript="Visual Studio Code: Go to Top"),
        "Go to ( bottom | last line)":
            R(Key("c-end"), rdescript="Visual Studio Code: Go to Bottom"),
        "ee-ol":
            R(Key("end"), rdescript="Visual Studio Code: End Of Line"),
        "beol":
            R(Key("home"), rdescript="Visual Studio Code: Beginning of Line"),
        "Go back [<n>]":
            R(Key("a-left"), rdescript="Visual Studio Code: Go Back")*Repeat(extra="n"),
        "Go forward [<n>]":
            R(Key("a-right"), rdescript="Visual Studio Code: Go Forward")*
            Repeat(extra="n"),

        # Formatting
        "indent [<n>]":
            R(Key("tab"), rdescript="Visual Studio Code: Indent")*Repeat(extra="n"),
        "Unindent [<n>]":
            R(Key("s-tab"), rdescript="Visual Studio Code: Unindent")*Repeat(extra="n"),
        "Comment":
            R(Key("c-slash"), rdescript="Visual Studio Code: Line Comment"),
        "Block comment":
            R(Key("sa-a"), rdescript="Visual Studio Code: Block Comment"),

        # Window Management
        "[toggle] full screen":
            R(Key("f11"), rdescript="Visual Studio Code:Fullscreen"),
        "[toggle] Zen mode":
            R(Key("c-k/3, z")),

        # Debugging
        "[toggle] breakpoint":
            R(Key("f9"), rdescript="Visual Studio Code:Breakpoint"),
        "step over [<n>]":
            R(Key("f10/50")*Repeat(extra="n"), rdescript="Visual Studio Code:Step Over"),
        "step into":
            R(Key("f11"), rdescript="Visual Studio Code:Step Into"),
        "step out [of]":
            R(Key("s-f11"), rdescript="Visual Studio Code:Step Out"),
        "resume":
            R(Key("f5"), rdescript="Visual Studio Code:Resume"),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1, "mim": "", "text": ""}


#---------------------------------------------------------------------------

context = AppContext(executable="code")
grammar = Grammar("Visual Studio Code", context=context)
if settings.SETTINGS["apps"]["visualstudiocode"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(VisualStudioCodeRule())
    else:
        rule = VisualStudioCodeRule(name="visualstudiocode")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
