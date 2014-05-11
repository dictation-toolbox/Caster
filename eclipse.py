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
            "close (editor | tab) [<n>]":                Key("c-w") * Repeat(extra="n"),
            "open resource":                    Key("cs-r"),
            "open type":                    Key("cs-t"),
            "go to line":                Key("c-l"),
            "go to line <n>":                Key("c-l") + Pause("50") + Text("%(n)d") + Key("enter"),
            "go to declaration":                Key("f3"),
            "cancel":                    Key("escape"),
            "editor select":                Key("c-e"),
            "pop":                Key("c-space, down, up"),
            
            "color left [<n>]":                Key("cs-left") * Repeat(extra="n"),
            "color right [<n>]":               Key("cs-right") * Repeat(extra="n"),
            "color up [<n>]":               Key("shift:down, up, shift:up") * Repeat(extra="n"),
            "color down [<n>]":               Key("shift:down, down, shift:up") * Repeat(extra="n"),

            "step [<n>]":                Key("f6") * Repeat(extra="n"),
            "step into":                Key("f5"),
            "step out [of]":                Key("f7"),
            "debug last":                Key("f11"),
            
            "show (java | coffee) perspective":                Key("cas-j"),
            "show debug perspective":                Key("cas-d"),
            "show python perspective":                Key("cas-p"),
            
       "format code":            Key("cs-f"),
       "(do imports | import all)":    Key("cs-o"),
        "comment line":                  Key("c-slash"),
        
        "space [<n>]":                      Key("space:%(n)d"),
           "enter [<n>]":                      Key("enter:%(n)d"),
           "tab [<n>]":                        Key("tab:%(n)d"),
           "delete [<n>]":                     Key("del:%(n)d"),
           "delete [<n> | this] (line|lines)": Key("home, s-down:%(n)d, del"),
           "backspace [<n>]":                  Key("backspace:%(n)d"),
           "pop up":                           Key("apps"),

           "paste":                            Key("c-v"),
           "duplicate <n>":                    Key("c-c, c-v:%(n)d"),
           "copy":                             Key("c-c"),
           "cut":                              Key("c-x"),
           "select all":                       Key("c-a"),
           "[hold] shift":                     Key("shift:down"),
           "release shift":                    Key("shift:up"),
           "[hold] control":                   Key("ctrl:down"),
           "release control":                  Key("ctrl:up"),  
        
        }
    extras = [
              Dictation("text"),
              Dictation("dict2"),
              IntegerRef("1to9", 1, 10),
              IntegerRef("n", 1, 100),
              NumberRef("int2"),
              Choice("zoom",
                    {"75": "7", "100": "1", "page width": "p",
                     "text width": "t", "whole page": "w",
                    }),
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
