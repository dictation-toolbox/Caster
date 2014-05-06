#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for Excel

"""


#---------------------------------------------------------------------------

from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, Choice, IntegerRef, NumberRef,
                       Key, Text, Repeat)


class CommandRule(MappingRule):

    mapping = {
        "give alpha [<level>]":                    Key("s-a, enter") * Repeat(extra="level"),
        "give beta [<level>]":                    Key("s-b, enter") * Repeat(extra="level"),
        "give charlie [<level>]":                    Key("s-c, enter") * Repeat(extra="level"),
        "give delta [<level>]":                    Key("s-d, enter") * Repeat(extra="level"),
        "skip [<level>]":                    Key("enter") * Repeat(extra="level"),
        
        }
    extras = [
              Dictation("dict"),
              Dictation("dict2"),
              IntegerRef("1to9", 1, 10),
              IntegerRef("level",1, 100),
              NumberRef("int2"),
              Choice("zoom",
                    {"75": "7", "100": "1", "page width": "p",
                     "text width": "t", "whole page": "w",
                    }),
             ]
    defaults ={"level": 1}

#---------------------------------------------------------------------------

context = AppContext(executable="excel")
grammar = Grammar("Microsoft Excel", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None