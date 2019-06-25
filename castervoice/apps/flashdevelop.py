from castervoice.lib.imports import *


class FlashDevelopRule(MergeRule):
    pronunciation = "flash develop"

    mapping = {
        "prior tab [<n>]": R(Key("c-pgup"))*Repeat(extra="n"),
        "next tab [<n>]": R(Key("c-pgdown"))*Repeat(extra="n"),
        "open resource": R(Key("c-r")),
        "jump to source": R(Key("f4")),
        "jump away": R(Key("s-f4")),
        "step over [<n>]": R(Key("f10")*Repeat(extra="n")),
        "step into": R(Key("f11")),
        "step out [of]": R(Key("s-f11")),
        "resume": R(Key("a-d, c")),
        "terminate": R(Key("s-f5")),
        "find everywhere": R(Key("cs-f")),
        "refractor symbol": R(Key("a-r, r")),
        "symbol next [<n>]": R(Key("f3"))*Repeat(extra="n"),
        "symbol prior [<n>]": R(Key("s-f3"))*Repeat(extra="n"),
        "format code": R(Key("cs-2")),
        "comment line": R(Key("c-q")),
        "clean it": R(Key("s-f8")),
        "build it": R(Key("f8")),
        "(debug | run) last": R(Key("f5")),
        "split view horizontal": R(Key("cs-enter")),
        "auto complete": R(Key("cs-1")),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1, "mim": ""}


class FlashDevelopCCR(MergeRule):
    pronunciation = "flash develop"
    non = FlashDevelopRule

    mapping = {
        "[go to] line <n>": R(Key("c-g") + Pause("50") + Text("%(n)d") + Key("enter")),
    }
    extras = [
        Dictation("text"),
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1}


context = AppContext(executable="FlashDevelop", title="FlashDevelop")
control.ccr_app_rule(FlashDevelopCCR(), context=context)