from dragonfly import (Grammar, Dictation, Repeat)

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R


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


context = AppContext(executable="Foxit Reader")
control.non_ccr_app_rule(FoxitRule(), context=context)