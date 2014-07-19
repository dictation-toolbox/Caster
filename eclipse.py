#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for ECLIPSE

"""


#---------------------------------------------------------------------------

from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, Choice, IntegerRef, NumberRef,
                       Key, Text, Repeat, Pause)


class CommandRule(MappingRule):

    mapping = {
        
           
            "previous (editor | tab) [<n>]":            Key("cs-f6") * Repeat(extra="n"),  # these two must be set up in the eclipse preferences
            "next (editor | tab) [<n>]":                Key("c-f6") * Repeat(extra="n"),
            "close (editor | tab) [<n>]":               Key("c-w") * Repeat(extra="n"),
            "open resource":                            Key("cs-r"),
            "open type":                                Key("cs-t"),
#             "go to line":                               Key("c-l"),
            "[go to] line <n>":                         Key("c-l") + Pause("50") + Text("%(n)d") + Key("enter"),
            "go to declaration":                        Key("f3"),
            "editor select":                            Key("c-e"),
            "pop":                                      Key("c-space, down, up"),
            
            "step [<n>]":                               Key("f6") * Repeat(extra="n"),
            "step into":                                Key("f5"),
            "step out [of]":                            Key("f7"),
            "(debug | run) last":                       Key("f11"),
            
            "show (java | coffee) perspective":         Key("cas-j"),
            "show debug perspective":                   Key("cas-d"),
            "show python perspective":                  Key("cas-p"),
            
            
            "format code":                              Key("cs-f"),
            "(do imports | import all)":                Key("cs-o"),
            "comment line":                             Key("c-slash"),
            
            # requires quick bookmarks plug-in:
            "set mark [<n>]":                           Key("a-%(n)d"),
            "go mark [<n>]":                            Key("as-%(n)d"),
        }
    extras = [
              Dictation("text"),
              IntegerRef("n", 1, 1000),
              
             ]
    defaults = {"n": 1}

#---------------------------------------------------------------------------

context = AppContext(executable="eclipse")
grammar = Grammar("Eclipse", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
