#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for Notepad++

"""


#---------------------------------------------------------------------------

from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, IntegerRef, Mouse,
                       Key, Text, Repeat, Pause)


class CommandRule(MappingRule):

    mapping = {
            "next tab [<n>]":                       Key("c-pgdown") * Repeat(extra="n"),
            "previous tab [<n>]":                   Key("c-pgup") * Repeat(extra="n"),
            "close tab [<n>]":                      Key("c-w") * Repeat(extra="n"),
            
            "stylize <n2>":                         Mouse("right")+Key("down:6/5, right")+(Key("down") * Repeat(extra="n2"))+Key("enter"),
            "remove style":                         Mouse("right")+Key("down:6/5, right/5, down:5/5, enter"),
            
            "preview in chrome":                    Key("cas-r"),
            # requires function list plug-in:
            "function list":                        Key("cas-l"),
        }
    extras = [
              Dictation("text"),
              IntegerRef("n", 1, 100),
              IntegerRef("n2", 1, 10),
              
             ]
    defaults = {"n": 1}

#---------------------------------------------------------------------------

context = AppContext(executable="notepad++")
grammar = Grammar("Notepad++", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
