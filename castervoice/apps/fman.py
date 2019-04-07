from dragonfly import (Grammar, Pause, Choice)

from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext

from castervoice.lib import control, settings
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R

class fmanRule(MergeRule):
    pronunciation = "F man"

    mapping = {
        "copy":
            R(Key("f5"), rdescript="Fman: copy"),
        "deselect":
            R(Key("c-d"), rdescript="Fman: deselect"),
        "edit":
            R(Key("f4"), rdescript="Fman: edit"),
        "explorer":
            R(Key("f10"), rdescript="Fman: explorer"),
        # Set these yourself and add them to the Choice at the bottom
        # Requires the favourites plug-in
        "go <fav>":
            R(Key("c-0") + Pause("15") + Text("%(fav)s") + Key("enter"), rdescript="Fman: go <favorite>"),
        "go see":
            R(Key("c-p") + Pause("15") + Text("c") + Key("enter"), rdescript="Fman: go see"),
        "go to":
            R(Key("c-p"), rdescript="Fman: go to"),
        "move":
            R(Key("f6"), rdescript="Fman: move"),
        "new file":
            R(Key("s-f4"), rdescript="Fman: new file"),
        "new folder":
            R(Key("f7"), rdescript="Fman: new folder"),
        "open left":
            R(Key("c-left"), rdescript="Fman: open left"),
        "open right":
            R(Key("c-right"), rdescript="Fman: open right"),
        "properties":
            R(Key("a-enter"), rdescript="Fman: properties"),
        "refresh":
            R(Key("c-r"), rdescript="Fman: refresh"),
        "rename":
            R(Key("s-f6"), rdescript="Fman: rename"),
        "search":
            R(Key("cs-f"), rdescript="Fman: search"),
        "set favourite":
            R(Key("s-f"), rdescript="Fman: set favourite"),
        "show favourites":
            R(Key("c-0"), rdescript="Fman: show favourites"),
        "(show | hide) hidden":
            R(Key("c-dot"), rdescript="Fman: toggle hidden"),
        "sort [by] name":
            R(Key("c-f1"), rdescript="Fman: Sort by name"),
        "sort [by] size":
            R(Key("c-f2"), rdescript="Fman: Sort by size"),
        "sort [by] (modified | date)":
            R(Key("c-f3"), rdescript="Fman: Sort by modified or date"),
        "(stoosh | copy) path":
            R(Key("f11"), rdescript="Fman: copy path"),
        "terminal":
            R(Key("f9"), rdescript="Fman: terminal"),
        "command pallette":
            R(Key("cs-p"), rdescript="Fman: Command Pallette"),

    }

    extras = [
        IntegerRefST("num", 1, 4),
        Choice("fav", {
            "example favourite":"ef",
        }),
    ]
    defaults = {
        "num":1,
    }


context = AppContext(executable="fman", title="fman")
grammar = Grammar("fman", context=context)
if settings.SETTINGS["apps"]["fman"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(fmanRule())
    else:
        rule = fmanRule()
        gfilter.run_on(rule)
        grammar.add_rule(fmanRule(name="fman"))
        grammar.load()
