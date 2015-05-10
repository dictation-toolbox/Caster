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


class CommandRule(MappingRule):

    mapping = {
            "run this query":                       Key("f9"),
            "format code":                          Key("c-f7"),
            "comment line":                         Key("c-slash"),
            
        }
    extras = [
              Dictation("text"),
              IntegerRef("n", 1, 1000),
              
             ]
    defaults = {"n": 1}

#---------------------------------------------------------------------------

context = AppContext(executable="sqldeveloper64W", title="SQL Developer") 
grammar = Grammar("Sql Developer", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
