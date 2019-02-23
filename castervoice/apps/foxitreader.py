from dragonfly import (Grammar, Dictation, Repeat)

from caster.lib import control
from caster.lib import settings
from caster.lib.actions import Key
from caster.lib.context import AppContext
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


class FoxitRule(MergeRule):
    pronunciation = "fox it reader"

    mapping = {
        "next tab [<n>]":
            R(Key("c-tab"), rdescript="Foxit Reader: Next Tab")*Repeat(extra="n"),
        "prior tab [<n>]":
            R(Key("cs-tab"), rdescript="Foxit Reader: Previous Tab")*Repeat(extra="n"),
        "close tab [<n>]":
            R(Key("c-f4/20"), rdescript="Foxit Reader: Close Tab")*Repeat(extra="n"),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1, "mim": ""}


#---------------------------------------------------------------------------

context = AppContext(executable="Foxit Reader")
grammar = Grammar("Foxit Reader", context=context)

if settings.SETTINGS["apps"]["foxitreader"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(FoxitRule())
    else:
        rule = FoxitRule(name="Foxit Reader")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
