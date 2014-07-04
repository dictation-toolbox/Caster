#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for VLC

"""


#---------------------------------------------------------------------------

from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, Choice, IntegerRef, NumberRef,
                       Key, Text, Repeat)


class CommandRule(MappingRule):

    mapping = {
        "tick forward [<n>]":               Key("s-right") * Repeat(extra="n"),
        "tick back [<n>]":                  Key("s-left") * Repeat(extra="n"),
        "forward [<n>]":                    Key("c-left") * Repeat(extra="n"),
        "back [<n>]":                       Key("c-left") * Repeat(extra="n"),
        
        
        }
    extras = [
              Dictation("dict"),
              IntegerRef("n", 1, 10),
              Choice("zoom",
                    {"75": "7", "100": "1", "page width": "p",
                     "text width": "t", "whole page": "w",
                    }),
             ]
    defaults ={"n": 1}

#---------------------------------------------------------------------------

context = AppContext(executable="vlc")
grammar = Grammar("vlc", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None