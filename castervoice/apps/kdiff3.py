from dragonfly import (Grammar, Dictation)

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R


class KDiff3Rule(MergeRule):
    pronunciation = "K diff"

    mapping = {
        "refresh": R(Key("f5"), rdescript="Kdiff3: Refresh"),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1, "mim": ""}


context = AppContext(executable="kdiff3")
control.non_ccr_app_rule(KDiff3Rule(), context=context)