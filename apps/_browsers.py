#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for Chrome and Firefox

"""

#---------------------------------------------------------------------------

from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, IntegerRef, Function,
                       Key, Text, Repeat)

    

class CommandRule(MappingRule):

    mapping = {
        "close tab [<n>]":              Key("c-w/20") * Repeat(extra="n"),
        "new tab [<n>]":                Key("c-t") * Repeat(extra="n"),
        "reopen tab [<n>]":             Key("cs-t") * Repeat(extra="n"),
        "next tab [<n>]":               Key("c-tab") * Repeat(extra="n"),
        "previous tab [<n>]":           Key("cs-tab") * Repeat(extra="n"),
        "show history":                 Key("c-h"),
        "show downloads":               Key("c-j"),
        "zoom in <n>":                  Key("c-plus/20") * Repeat(extra="n"),
        "zoom out <n>":                 Key("c-minus/20") * Repeat(extra="n"),
        "refresh":                      Key("c-r"),
        "[add] bookmark":               Key("c-d"),
        
        "developer tools":              Key("f12"),
        "resume":                       Key("f8"),
        "step over":                    Key("f10"),
        "step into":                    Key("f11"),
        "step out":                     Key("s-f11"),
        
        "IRC identify":                 Text("/msg NickServ identify PASSWORD"),
        }
    extras = [
              Dictation("dict"),
              IntegerRef("n",1, 100),
             ]
    defaults ={"n": 1, "dict":"nothing"}


#---------------------------------------------------------------------------

context = AppContext(executable="chrome") | AppContext(executable="firefox")
grammar = Grammar("browsers", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None