#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for git

"""


#---------------------------------------------------------------------------

from dragonfly import (Grammar, AppContext, MappingRule,
                       Key, Text)


class CommandRule(MappingRule):

    mapping = {
        "C drive":          Text("cd C:\\")+Key("enter"),
        "CD up":            Text( "cd .." )+Key("enter"),
        "CD":               Text( "cd " ),
        "list":             Text( "dir" )+Key("enter"),
        "make directory":   Text( "mkdir " ),
        
        
        
        "exit":             Text( "exit" )+Key("enter"),
        }
    extras = [
              
             ]
    defaults ={}


#---------------------------------------------------------------------------

context = AppContext(executable="cmd")
grammar = Grammar("cmd", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None