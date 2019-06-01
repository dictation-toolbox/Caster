'''
Mike Roberts 13/09/18
'''

from dragonfly import (Dictation, Grammar, IntegerRef, MappingRule, Pause,
                       Repeat, Mimic, ShortIntegerRef, Function, Choice)

from castervoice.lib import control, settings, navigation
from castervoice.lib.actions import Key, Text
from castervoice.lib.temporary import Store, Retrieve
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R

class RStudioRule(MergeRule):
    pronunciation = "are studio"

    mapping = {
    "new file":
        R(Key("cs-n")),
    "open file":
        R(Key("c-o")),
    "open recent project":
        R(Key("a-f, j")),
  	"open project":
        R(Key("a-f, n, enter")),
    "save all":
        R(Key("ac-s")),
    "select all":
        R(Key("c-a")),
    "find":
        R(Key("c-f")),

    "[go to] line <ln1>":
        R(Key("as-g") + Pause("10") + Text("%(ln1)s") + Key("enter")),
    "<action> [line] <ln1> [by <ln2>]"  :
        R(Function(navigation.action_lines, go_to_line="as-g/10", select_line_down="s-down", wait="/3")),

    "focus console":
        R(Key("c-2")),
    "focus main":
        R(Key("c-1")),

    "next tab":
        R(Key("c-f12")),
    "first tab":
        R(Key("cs-f11")),
    "previous tab":
        R(Key("c-f11")),
    "last tab":
        R(Key("cs-f12")),
    "close tab":
        R(Key("c-w")),


    "run line":
        R(Key("c-enter")),
    "run document":
        R(Key("ac-r")),
    "comment (line | selected)":
        R(Key("cs-c")),

    "next plot":
        R(Key("ac-f12")),
    "previous plot":
        R(Key("ac-f11")),

    "(help | document) that":
        R(Store() + Key("c-2, question") + Retrieve() + Key("enter, c-3")),
    "glimpse that":
        R(Store() + Key("c-2") + Retrieve() + Key("space, percent, rangle, percent") + Text(" glimpse()") + Key("enter/50, c-1")),
    "vee table that":
        R(Store() + Key("c-2") + Text("library(vtable)") + Key("enter/50") + Retrieve() + Key("space, percent, rangle, percent") + Text(" vtable()") + Key("enter/50, c-1")),

    }
    extras = [
        ShortIntegerRef("ln1", 1, 10000),
        ShortIntegerRef("ln2", 1, 10000),
        Choice("action", navigation.actions),
    ]
    defaults = {"ln2": ""}

context = AppContext(executable="rstudio")
grammar = Grammar("RStudio", context=context)
if settings.SETTINGS["apps"]["rstudio"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(RStudioRule())
    else:
        rule = RStudioRule()
        gfilter.run_on(rule)
        grammar.add_rule(RStudioRule(name="rstudio"))
        grammar.load()
