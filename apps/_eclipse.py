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
                       Dictation, IntegerRef,
                       Key, Text, Repeat, Pause)
from dragonfly.actions.action_function import Function
from dragonfly.actions.action_mimic import Mimic


class CommandRule(MappingRule):

    mapping = {
                    
            "previous (editor | tab) [<n>]":            Key("cs-f6") * Repeat(extra="n"),  # these two must be set up in the eclipse preferences
            "next (editor | tab) [<n>]":                Key("c-f6") * Repeat(extra="n"),
            "close (editor | tab) [<n>]":               Key("c-w") * Repeat(extra="n"),
            "open resource":                            Key("cs-r"),
            "open type":                                Key("cs-t"),

            "[go to] line <n> [<mim>]":                 Key("c-l") + Pause("50") + Text("%(n)d") + Key("enter")+ Pause("50")+Mimic(extra="mim"),
            "go to declaration":                        Key("f3"),
            "editor select":                            Key("c-e"),
            "pop":                                      Key("c-space, down, up"),
            
            "step over [<n>]":                          Key("f6/50") * Repeat(extra="n"),
            "step into":                                Key("f5"),
            "step out [of]":                            Key("f7"),
            "resume":                                   Key("f8"),
            "(debug | run) last":                       Key("f11"),
            
            "show (java | coffee) perspective":         Key("cas-j"),
            "show debug perspective":                   Key("cas-d"),
            "show python perspective":                  Key("cas-p"),
            
            
            "format code":                              Key("cs-f"),
            "do imports":                               Key("cs-o"),
            "comment line":                             Key("c-slash"),
            
            # requires quick bookmarks plug-in:
            "set mark [<n>]":                           Key("a-%(n)d"),
            "go mark [<n>]":                            Key("as-%(n)d"),
        }
    extras = [
              Dictation("text"),
              Dictation("mim"),
              IntegerRef("n", 1, 1000),
              
             ]
    defaults = {"n": 1, "mim":""}

#---------------------------------------------------------------------------

context = AppContext(executable="eclipse") | AppContext(executable="AptanaStudio3")
grammar = Grammar("Eclipse", context=context)
grammar.add_rule(CommandRule())
grammar.load()
#Digital and 66 go to line 66;;some words cohere
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
