#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for pythonw

"""


#---------------------------------------------------------------------------

from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, Choice, IntegerRef, NumberRef,
                       Key, Text, Repeat,BringApp)
import paths
BASE_PATH=paths.get_base()

class CommandRule(MappingRule):

    mapping = {
        'help':               Key("question")        
        }
    extras = [
              Dictation("dict"),
              Dictation("dict2"),
              IntegerRef("number", 1, 100),
              NumberRef("int2"),
              Choice("zoom",
                    {"75": "7", "100": "1", "page width": "p",
                     "text width": "t", "whole page": "w",
                    }),
             ]
    defaults ={"level": 1}

#---------------------------------------------------------------------------

context = AppContext(executable="pythonw")
grammar = Grammar("Custom Grid", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None