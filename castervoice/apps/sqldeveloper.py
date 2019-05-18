#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""
Command-module for Sql Developer

"""
#---------------------------------------------------------------------------

from dragonfly import (Grammar, Dictation)

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R


class SQLDeveloperRule(MergeRule):
    pronunciation = "sequel developer"

    mapping = {
        "run this query": R(Key("f9"), rdescript="SQL Dev: Run Query"),
        "format code": R(Key("c-f7"), rdescript="SQL Dev: Format Code"),
        "comment line": R(Key("c-slash"), rdescript="SQL Dev: Comment Line"),
    }
    extras = [
        Dictation("text"),
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1}


#---------------------------------------------------------------------------

context = AppContext(executable="sqldeveloper64W", title="SQL Developer")
grammar = Grammar("Sql Developer", context=context)

if settings.SETTINGS["apps"]["sqldeveloper"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(SQLDeveloperRule())
    else:
        rule = SQLDeveloperRule(name="sql developer")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
