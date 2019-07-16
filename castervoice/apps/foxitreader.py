from castervoice.lib.imports import *

class FoxitRule(MergeRule):
    pronunciation = "fox it reader"

    mapping = {
        "next tab [<n>]": R(Key("c-tab"))*Repeat(extra="n"),
        "prior tab [<n>]": R(Key("cs-tab"))*Repeat(extra="n"),
        "close tab [<n>]": R(Key("c-f4/20"))*Repeat(extra="n"),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1, "mim": ""}


context = AppContext(executable="Foxit Reader")
control.non_ccr_app_rule(FoxitRule(), context=context)