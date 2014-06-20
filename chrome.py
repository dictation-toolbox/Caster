#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for Chrome

"""


#---------------------------------------------------------------------------

from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, Choice, IntegerRef, NumberRef,
                       Key, Text, Repeat, Pause)


class CommandRule(MappingRule):

    mapping = {
        "close tab [<n>]":            (Key("c-w")+Pause("10")) * Repeat(extra="n"),
        "new tab [<n>]":                    	Key("c-t") * Repeat(extra="n"),
        "reopen tab [<n>]":                   Key("cs-t") * Repeat(extra="n"),
        "next tab [<n>]":                        Key("c-tab") * Repeat(extra="n"),
        "previous tab [<n>]":                        Key("cs-tab") * Repeat(extra="n"),
        "show history":               Key("c-h"),
        "show downloads":               Key("c-j"),
        "zoom in <n>":              Key("c-plus") * Repeat(extra="n"),
        "zoom out <n>":             Key("c-minus") * Repeat(extra="n"),
        "refresh":            Key("c-r"),
        "search for <dict>":               Key("c-t")+Pause("50")+ Text("%(dict)s"),
        "git hub":          Text("github"),
        }
    extras = [
              Dictation("dict"),
              Dictation("dict2"),
              IntegerRef("1to9", 1, 10),
              IntegerRef("n",1, 100),
              NumberRef("int2"),
              Choice("zoom",
                    {"75": "7", "100": "1", "page width": "p",
                     "text width": "t", "whole page": "w",
                    }),
             ]
    defaults ={"n": 1}


#---------------------------------------------------------------------------

context = AppContext(executable="chrome")
grammar = Grammar("Google Chrome", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None