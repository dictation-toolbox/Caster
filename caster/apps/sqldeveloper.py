#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""
Command-module for Sql Developer

"""
#---------------------------------------------------------------------------

from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, IntegerRef,
                       Key, Text, Repeat, Pause)

from caster.lib import settings
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.state.short import R


from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib import control


class CommandRule(MergeRule):
    pronunciation = "sequel developer"

    mapping = {
            "run this query":                       R(Key("f9"), rdescript="SQL Dev: Run Query"),
            "format code":                          R(Key("c-f7"), rdescript="SQL Dev: Format Code"),
            "comment line":                         R(Key("c-slash"), rdescript="SQL Dev: Comment Line"),
            
        }
    extras = [
              Dictation("text"),
              IntegerRefST("n", 1, 1000),
              
             ]
    defaults = {"n": 1}

#---------------------------------------------------------------------------

context = AppContext(executable="sqldeveloper64W", title="SQL Developer") 
grammar = Grammar("Sql Developer", context=context)
grammar.add_rule(CommandRule(name="sql developer"))
if settings.SETTINGS["apps"]["sqldeveloper"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(CommandRule())
    else:
        grammar.load()