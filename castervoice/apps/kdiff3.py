from castervoice.lib.imports import *

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