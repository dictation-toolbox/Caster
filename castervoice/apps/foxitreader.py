from castervoice.lib.imports import *

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