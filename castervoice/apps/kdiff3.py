from dragonfly import (Grammar, Dictation)

from caster.lib import control
from caster.lib import settings
from caster.lib.actions import Key
from caster.lib.context import AppContext
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


class KDiff3Rule(MergeRule):
    pronunciation = "K diff"

    mapping = {
        "refresh": R(Key("f5"), rdescript="Refresh"),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1, "mim": ""}


#---------------------------------------------------------------------------

context = AppContext(executable="kdiff3")
grammar = Grammar("KDiff3", context=context)

if settings.SETTINGS["apps"]["kdiff3"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(KDiff3Rule())
    else:
        rule = KDiff3Rule(name="kdiff3")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
