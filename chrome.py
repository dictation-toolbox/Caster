#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for ECLIPSE

"""


#---------------------------------------------------------------------------

from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, Choice, IntegerRef, NumberRef,
                       Key, Text, Repeat)


#---------------------------------------------------------------------------
# Create the main command rule.

class CommandRule(MappingRule):

    mapping = {
        "close tab":                    Key("c-w"),
        "new tab":                    	Key("c-t"),
        "reopen tab":                   Key("cs-t"),
        "next tab":                        Key("c-tab"),
        "last tab":                        Key("cs-tab"),
        
        }
    extras = [
              Dictation("dict"),
              Dictation("dict2"),
              IntegerRef("1to9", 1, 10),
              NumberRef("int"),
              NumberRef("int2"),
              Choice("zoom",
                    {"75": "7", "100": "1", "page width": "p",
                     "text width": "t", "whole page": "w",
                    }),
             ]


#---------------------------------------------------------------------------

context = AppContext(executable="chrome")
grammar = Grammar("Google Chrome", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None