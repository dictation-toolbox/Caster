#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for Ultima Online

"""


#---------------------------------------------------------------------------

from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, Choice, IntegerRef, NumberRef,
                       Key, Text, Repeat)


class CommandRule(MappingRule):

    mapping = {
        "war and peace":                   Key("c-a") ,
        "hide":                    Key("c-h") ,
        "talk town":                    Key("c-b") ,
        "last item":                    Key("c-i") ,
        "last skill":                    Key("c-l") ,
        "provoke":                    Key("c-p") ,
        "don't kill me":                    Key("a-p") ,
        "say <dict>":                           Text("%(dict)s"),
        "clear [<level>]":                Key("backspace")* Repeat(extra="level"),
        "give delta [<level>]":                    Key("s-d, enter") * Repeat(extra="level"),
        "skip [<level>]":                    Key("enter") * Repeat(extra="level"),
        
        }
    extras = [
              Dictation("dict"),
              Dictation("dict2"),
              IntegerRef("1to9", 1, 10),
              IntegerRef("level",1, 1000),
              NumberRef("int2"),
              Choice("zoom",
                    {"75": "7", "100": "1", "page width": "p",
                     "text width": "t", "whole page": "w",
                    }),
             ]
    defaults ={"level": 1}

#---------------------------------------------------------------------------

context = AppContext(executable="client")
grammar = Grammar("Ultima Online", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None