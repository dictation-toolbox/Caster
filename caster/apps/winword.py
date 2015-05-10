#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for word

"""


#---------------------------------------------------------------------------

from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, Playback, IntegerRef, Function,
                       Key, Text, Repeat, WaitWindow, Mouse, Pause)


    

class CommandRule(MappingRule):

    mapping = {
        "insert image":              Key("alt, n, p"),
        
        
        }
    extras = [
              Dictation("dict"),
              IntegerRef("n",1, 100),
             ]
    defaults ={"n": 1, "dict":"nothing"}


#---------------------------------------------------------------------------

context = AppContext(executable="winword")
grammar = Grammar("Microsoft Word", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None