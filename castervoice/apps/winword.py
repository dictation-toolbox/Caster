#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""
Command-module for word

"""
#---------------------------------------------------------------------------

from dragonfly import (Grammar, MappingRule, Dictation)

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R


class MSWordRule(MergeRule):
    pronunciation = "Microsoft Word"

    mapping = {
        "insert image": R(Key("alt, n, p"), rdescript="Word: Insert Image"),
    }
    extras = [
        Dictation("dict"),
        IntegerRefST("n", 1, 100),
    ]
    defaults = {"n": 1, "dict": "nothing"}


#---------------------------------------------------------------------------

context = AppContext(executable="winword")
grammar = Grammar("Microsoft Word", context=context)

if settings.SETTINGS["apps"]["winword"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(MSWordRule())
    else:
        rule = MSWordRule(name="microsoft word")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
