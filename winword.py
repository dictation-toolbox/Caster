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
            "underscore [<n>]":                 Key("underscore")*Repeat(extra="n"),
            "center":                           Key("c-e"),
        }
    extras = [
              Dictation("dict"),
              IntegerRef("n", 1, 30),
              Choice("zoom",
                    {"75": "7", "100": "1", "page width": "p",
                     "text width": "t", "whole page": "w",
                    }),
             ]
    defaults ={"n": 1}

#---------------------------------------------------------------------------

context = AppContext(executable="winword")
grammar = Grammar("Microsoft Word", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None