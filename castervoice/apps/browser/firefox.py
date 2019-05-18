#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""
Command-module for Firefox

"""
#---------------------------------------------------------------------------

from dragonfly import (Grammar, Dictation, Repeat)

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R


class FirefoxRule(MergeRule):
    pronunciation = "fire fox"

    mapping = {
        "new tab [<n>]":
            R(Key("c-t"), rdescript="FireFox: New Tab")*Repeat(extra="n"),
        "reopen tab [<n>]":
            R(Key("cs-t"), rdescript="FireFox: Reopen Tab")*Repeat(extra="n"),
        "show history":
            R(Key("c-h"), rdescript="FireFox: Show History"),
        "show downloads":
            R(Key("c-j"), rdescript="FireFox: Show Downloads"),
        "zoom in <n>":
            R(Key("c-plus/20"), rdescript="FireFox: Zoom In")*Repeat(extra="n"),
        "zoom out <n>":
            R(Key("c-minus/20"), rdescript="FireFox: Zoom")*Repeat(extra="n"),
        "super refresh":
            R(Key("c-f5"), rdescript="FireFox: Super Refresh"),
        "[add] bookmark":
            R(Key("c-d"), rdescript="FireFox: Add Bookmark"),
        "developer tools":
            R(Key("f12"), rdescript="FireFox: Developer Tools"),
        "resume":
            R(Key("f8"), rdescript="FireFox: Resume"),
        "step over":
            R(Key("f10"), rdescript="FireFox: Step Over"),
        "step into":
            R(Key("f11"), rdescript="FireFox: Step Into"),
        "step out":
            R(Key("s-f11"), rdescript="FireFox: Step Out"),
        "IRC identify":
            R(Text("/msg NickServ identify PASSWORD"),
              rdescript="FireFox: IRC Chat Channel Identify"),
    }
    extras = [
        Dictation("dict"),
        IntegerRefST("n", 1, 100),
    ]
    defaults = {"n": 1, "dict": "nothing"}


#---------------------------------------------------------------------------

context = AppContext(executable="firefox")
grammar = Grammar("firefox", context=context)

if settings.SETTINGS["apps"]["firefox"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(FirefoxRule())
    else:
        rule = FirefoxRule(name="firefox")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
