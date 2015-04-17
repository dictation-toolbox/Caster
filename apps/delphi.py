#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for but Delphi IDE

"""


#---------------------------------------------------------------------------

from dragonfly import (Grammar, AppContext, MappingRule,
                       Key, Text, Repeat, IntegerRef)


class CommandRule(MappingRule):

    mapping = {
         "step [over] [<n>]":        Key("f8/10") * Repeat(extra="n"),
         "step into":                Key("f7"),
         "run last":                 Key("f9"),
         "terminate":                Key("c-f2"),
         "add watch":                Key("c-f5"),
         "evaluate":                 Key("c-f7"),
         "symbol next":              Key("f3"),
         "go to line":               Key("a-g"),

         
        
        }
    extras = [
              IntegerRef("n", 1, 50),
              ]
    defaults = {
                "n": 1
                }


#---------------------------------------------------------------------------

context = AppContext(executable="delphi32")
grammar = Grammar("delphi", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
