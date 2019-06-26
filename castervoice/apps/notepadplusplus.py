from castervoice.lib.imports import *

class NPPRule(MergeRule):
    pronunciation = "notepad plus plus"

    mapping = {
        "stylize <n2>":
            R(Mouse("right") + Key("down:6/5, right") +
              (Key("down")*Repeat(extra="n2")) + Key("enter")),
        "remove style":
            R(Mouse("right") + Key("down:6/5, right/5, down:5/5, enter")),
        "preview in browser":
            R(Key("cas-r")),

        # requires function list plug-in:
        "function list":
            R(Key("cas-l")),
        "open":
            R(Key("c-o")),
        "go [to] line <n>":
            R(Key("c-g/10") + Text("%(n)s") + Key("enter")),
    }
    extras = [
        Dictation("text"),
        IntegerRefST("n", 1, 1000),
        IntegerRefST("n2", 1, 10),
    ]
    defaults = {"n": 1}


context = AppContext(executable="notepad++")
control.non_ccr_app_rule(NPPRule(), context=context)