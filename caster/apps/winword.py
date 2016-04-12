#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""
Command-module for word

"""
#---------------------------------------------------------------------------

from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, Key)

from caster.lib import settings
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.state.short import R


from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib import control


class CommandRule(MergeRule):
    pronunciation = "Microsoft Word"

    mapping = {
        "insert image":              R(Key("alt, n, p"), rdescript="Word: Insert Image"),
        
        
        }
    extras = [
              Dictation("dict"),
              IntegerRefST("n",1, 100),
             ]
    defaults ={"n": 1, "dict":"nothing"}


#---------------------------------------------------------------------------

context = AppContext(executable="winword")
grammar = Grammar("Microsoft Word", context=context)
grammar.add_rule(CommandRule(name="microsoft word"))
if settings.SETTINGS["apps"]["winword"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(CommandRule())
    else:
        grammar.load()