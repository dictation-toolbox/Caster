from castervoice.lib.imports import *

class NPPRule(MergeRule):
    pronunciation = "notepad plus plus"

    mapping = {
        "stylize <n2>":
            R(Mouse("right") + Key("down:6/5, right") +
              (Key("down")*Repeat(extra="n2")) + Key("enter"),
              rdescript="Notepad++: Stylize"),
        "remove style":
            R(Mouse("right") + Key("down:6/5, right/5, down:5/5, enter"),
              rdescript="Notepad++: Remove Style"),
        "preview in browser":
            R(Key("cas-r"), rdescript="Notepad++: Preview In Browser"),

        # requires function list plug-in:
        "function list":
            R(Key("cas-l"), rdescript="Notepad++: Function List"),
        "open":
            R(Key("c-o"), rdescript="Notepad++: Open"),
        "go [to] line <n>":
            R(Key("c-g/10") + Text("%(n)s") + Key("enter"),
              rdescript="Notepad++: Go to Line #"),
    }
    extras = [
        Dictation("text"),
        IntegerRefST("n", 1, 1000),
        IntegerRefST("n2", 1, 10),
    ]
    defaults = {"n": 1}


context = AppContext(executable="notepad++")
control.non_ccr_app_rule(NPPRule(), context=context)