from castervoice.lib.imports import *

class MSWordRule(MergeRule):
    pronunciation = "Microsoft Word"

    mapping = {
        "insert image": R(Key("alt, n, p")),
    }
    extras = [
        Dictation("dict"),
        IntegerRefST("n", 1, 100),
    ]
    defaults = {"n": 1, "dict": "nothing"}


context = AppContext(executable="winword")
control.non_ccr_app_rule(MSWordRule(), context=context)