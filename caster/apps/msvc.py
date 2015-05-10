#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for MSVC

"""


#---------------------------------------------------------------------------

from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, IntegerRef,
                       Key, Text, Repeat, Pause)


class CommandRule(MappingRule):

    mapping = {
        
           
#             "previous (editor | tab) [<n>]":            Key("cs-f6") * Repeat(extra="n"),  # these two must be set up in the eclipse preferences
#             "next (editor | tab) [<n>]":                Key("c-f6") * Repeat(extra="n"),
#             "close (editor | tab) [<n>]":               Key("c-w") * Repeat(extra="n"),
#             "open resource":                            Key("cs-r"),
#             "open type":                                Key("cs-t"),
#  
#             "[go to] line <n>":                         Key("c-l") + Pause("50") + Text("%(n)d") + Key("enter"),
#             "go to declaration":                        Key("f3"),
#             "editor select":                            Key("c-e"),
#             "pop":                                      Key("c-space, down, up"),
             
            "step over [<n>]":                          Key("f10/50") * Repeat(extra="n"),
            "step into":                                Key("f11"),
            "step out [of]":                            Key("s-f11"),
            "resume":                                   Key("f8"),
            "build [last]":                             Key("ca-f7"),
            "debug [last]":                             Key("f5"),
            "comment out":                              Key("c-k/50, c-c"),
            "on comment out":                           Key("c-k/50, c-u"),
            
            "breakpoint":                               Key("f9"),
            
            "format code":                              Key("cs-f"),
            "(do imports | import all)":                Key("cs-o"),
            "comment line":                             Key("c-slash"),
        }
    extras = [
              Dictation("text"),
              IntegerRef("n", 1, 1000),
              
             ]
    defaults = {"n": 1}

#---------------------------------------------------------------------------

context = AppContext(executable="WDExpress")# | AppContext(executable="AptanaStudio3")
grammar = Grammar("WDExpress", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
