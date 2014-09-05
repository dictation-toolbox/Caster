#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for Switcher

"""


#---------------------------------------------------------------------------

from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, Choice, IntegerRef, NumberRef,
                       Key, Text, Repeat)


class CommandRule(MappingRule):

    mapping = {
        "(select | choose) <1to9>":                    Key("%(1to9)d"),
        
        
        }
    extras = [
              IntegerRef("1to9", 1, 10),
             ]
    defaults ={"level": 1}

#---------------------------------------------------------------------------

context = AppContext(executable="Switcher")
grammar = Grammar("Switcher", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None