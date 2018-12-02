from dragonfly import (Grammar, MappingRule, Dictation, Repeat, Pause)

from caster.lib import control
from caster.lib import settings
from caster.lib.actions import Key, Text
from caster.ccr.core.nav import Navigation
from caster.lib.context import AppContext
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


class FlashDevelopRule(MergeRule):
    pronunciation = "flash develop"

    mapping = {
        "prior tab [<n>]":
            R(Key("c-pgup"), rdescript="FlashDevelop: Previous Tab")*Repeat(extra="n"),
        "next tab [<n>]":
            R(Key("c-pgdown"), rdescript="FlashDevelop: Next Tab")*Repeat(extra="n"),
        "open resource":
            R(Key("c-r"), rdescript="FlashDevelop: Open Resource"),
        "jump to source":
            R(Key("f4"), rdescript="FlashDevelop: Jump To Source"),
        "jump away":
            R(Key("s-f4"), rdescript="FlashDevelop: Jump Away"),
        "step over [<n>]":
            R(Key("f10")*Repeat(extra="n"), rdescript="FlashDevelop: Step Over"),
        "step into":
            R(Key("f11"), rdescript="FlashDevelop: Step Into"),
        "step out [of]":
            R(Key("s-f11"), rdescript="FlashDevelop: Step Out"),
        "resume":
            R(Key("a-d, c"), rdescript="FlashDevelop: Resume"),
        "terminate":
            R(Key("s-f5"), rdescript="FlashDevelop: Terminate Running Program"),
        "find everywhere":
            R(Key("cs-f"), rdescript="FlashDevelop: Search Project"),
        "refractor symbol":
            R(Key("a-r, r"), rdescript="FlashDevelop: Re-Factor Symbol"),
        "symbol next [<n>]":
            R(Key("f3"), rdescript="FlashDevelop: Symbol Next")*Repeat(extra="n"),
        "symbol prior [<n>]":
            R(Key("s-f3"), rdescript="FlashDevelop: Symbol Prior")*Repeat(extra="n"),
        "format code":
            R(Key("cs-2"), rdescript="FlashDevelop: Format Code"),
        "comment line":
            R(Key("c-q"), rdescript="FlashDevelop: Comment Line"),
        "clean it":
            R(Key("s-f8"), rdescript="FlashDevelop: Clean"),
        "build it":
            R(Key("f8"), rdescript="FlashDevelop: Build"),
        "(debug | run) last":
            R(Key("f5"), rdescript="FlashDevelop: Run"),
        "split view horizontal":
            R(Key("cs-enter"), rdescript="FlashDevelop: Split View (H)"),
        "auto complete":
            R(Key("cs-1"), rdescript="FlashDevelop: Auto Complete"),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1, "mim": ""}


class FlashDevelopCCR(MergeRule):
    pronunciation = "flash develop test"
    mwith = [Navigation().get_pronunciation()]

    mapping = {
        "[go to] line <n>":
            R(Key("c-g") + Pause("50") + Text("%(n)d") + Key("enter"),
              rdescript="FlashDevelop: Go To Line"),
    }
    extras = [
        Dictation("text"),
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1}


#---------------------------------------------------------------------------

context = AppContext(executable="FlashDevelop", title="FlashDevelop")
grammar = Grammar("FlashDevelop", context=context)

if settings.SETTINGS["apps"]["flashdevelop"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(FlashDevelopRule())
        control.nexus().merger.add_global_rule(FlashDevelopCCR())
    else:
        control.nexus().merger.add_app_rule(FlashDevelopCCR(name="FlashDevelop"), context)

        rule = FlashDevelopRule()
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
