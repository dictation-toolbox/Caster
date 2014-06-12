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
                       Dictation, Choice, IntegerRef, 
                       Key, Text, Repeat,BringApp, Function)
import paths, utilities
BASE_PATH=paths.get_base()

def navigate_grid(n, n2, click):
    Key("c").execute()
    utilities.press_digits(n)
    Key("r").execute()
    utilities.press_digits(n2)
    Key("enter").execute()
    if not type=="0":
        Key(str(click)).execute()

class CommandRule(MappingRule):

    mapping = {
        'help':                 Key("question"),
        "<n> by <n2> [<click>]":Function(navigate_grid,extra={'n', 'n2','type'}),        
        }
    extras = [
              Dictation("dict"),
              Dictation("dict2"),
              IntegerRef("n", 1, 1000),
              IntegerRef("n2", 1, 1000),
              Choice("click",
                    {"default": "0", "left": "s", "double": "d",
                     "dub": "d", "right": "t",
                    }),
             ]
    defaults ={"n": 1,"type":"0"}

#---------------------------------------------------------------------------

context = AppContext(executable="pythonw")
grammar = Grammar("Custom Grid", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None