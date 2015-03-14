#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for but android studio

"""


#---------------------------------------------------------------------------

from dragonfly import (Grammar, AppContext, MappingRule,
                       Key, Text)


class CommandRule(MappingRule):

    mapping = {
        "quickfix":                 Key("a-enter"),
        "duplicate":                Key("c-d"),
        
        }
    extras = [
              
             ]
    defaults ={}


#---------------------------------------------------------------------------

context = AppContext(executable="studio64")
grammar = Grammar("android studio", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None