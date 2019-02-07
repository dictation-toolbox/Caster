#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""
Command-module for git

"""
#---------------------------------------------------------------------------

from dragonfly import (Grammar, MappingRule)

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R
from castervoice.lib.context import AppContext
from castervoice.lib.actions import (Key, Text)

class CMDRule(MergeRule):
    pronunciation = "command prompt"

    mapping = {
        "C drive": R(Text(r"cd C:/") + Key("enter"), rdescript="CMD: Go To C:"),
        "CD up": R(Text("cd ..") + Key("enter"), rdescript="CMD: Up Directory"),
        "CD": R(Text("cd "), rdescript="CMD: Navigate Directory"),
        "list": R(Text("dir") + Key("enter"), rdescript="CMD: List Files"),
        "make directory": R(Text("mkdir "), rdescript="CMD: Make directory"),
        "exit": R(Text("exit") + Key("enter"), rdescript="CMD: Exit"),
    }
    extras = []
    defaults = {}


#---------------------------------------------------------------------------

context = AppContext(executable="cmd")
grammar = Grammar("cmd", context=context)

if settings.SETTINGS["apps"]["cmd"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(CMDRule())
        print("added CMD")
    else:
        rule = CMDRule(name="command prompt")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
