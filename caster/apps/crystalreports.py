#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for Pervasive Crystal Reports

"""


#---------------------------------------------------------------------------

from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, IntegerRef,
                       Key, Text, Repeat, Pause)


class CommandRule(MappingRule):

    mapping = {
            "add group":                       Key("a-i/5, g"),
            "add text field":                  Key("a-i/5, x"),
            
        }
    extras = [
              Dictation("text"),
              IntegerRef("n", 1, 1000),
              
             ]
    defaults = {"n": 1}

#---------------------------------------------------------------------------

context = AppContext(executable="crw32", title="s") | AppContext(executable="javaw.exe", title="Pervasive Control Center")
grammar = Grammar("Crystal Reports", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
