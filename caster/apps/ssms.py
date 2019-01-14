from dragonfly import (Grammar, Dictation, Repeat)

from caster.lib import control
from caster.lib import settings
from caster.lib.actions import Key
from caster.lib.context import AppContext
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


class SSMSRule(MergeRule):
    pronunciation = "sequel server management studio"

    mapping = {
        # There doesn't seem to be a hotkey for sequential tab navigation in SSMS, but something is better than nothing...
        "next tab [<n>]":
            R(Key("c-tab"), rdescript="SSMS: Next Tab")*Repeat(extra="n"),
        "prior tab [<n>]":
            R(Key("cs-tab"), rdescript="SSMS: Previous Tab")*Repeat(extra="n"),
        "close tab [<n>]":
            R(Key("c-f4/20"), rdescript="SSMS: Close Tab")*Repeat(extra="n"),
        "go to line":
            R(Key("c-g"), rdescript="SSMS: Go To Line"),
        "comment line":
            R(Key("c-k, c-c"), rdescript="SSMS: Comment Selection"),
        "comment block":
            R(Key("c-k, c-c"), rdescript="SSMS: Comment Block"),
        "(un | on) comment line":
            R(Key("c-k/50, c-u"), rdescript="SSMS: Uncomment Selection"),
        "(un | on) comment block":
            R(Key("c-k/50, c-u"), rdescript="SSMS: Uncomment Block"),
        "[toggle] full screen":
            R(Key("sa-enter"), rdescript="SSMS: Fullscreen"),
        "(set | toggle) bookmark":
            R(Key("c-k, c-k"), rdescript="SSMS: Toggle Bookmark"),
        "next bookmark":
            R(Key("c-k, c-n"), rdescript="SSMS: Next Bookmark"),
        "prior bookmark":
            R(Key("c-k, c-p"), rdescript="SSMS: Previous Bookmark"),
        "[toggle] breakpoint":
            R(Key("f9"), rdescript="SSMS: Breakpoint"),
        "step over [<n>]":
            R(Key("f10/50")*Repeat(extra="n"), rdescript="SSMS: Step Over"),
        "step into":
            R(Key("f11"), rdescript="SSMS: Step Into"),
        "step out [of]":
            R(Key("s-f11"), rdescript="SSMS: Step Out"),
        "resume":
            R(Key("f5"), rdescript="SSMS: Resume"),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1, "mim": ""}


#---------------------------------------------------------------------------

context = AppContext(executable="ssms")
grammar = Grammar("SQL Server Management Studio", context=context)

if settings.SETTINGS["apps"]["ssms"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(SSMSRule())
    else:
        rule = SSMSRule(name="ssms")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
