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
from caster.lib.dfplus.state.short import R
    

class CommandRule(MappingRule):

    mapping = {
        "close tab [<n>]":              R(Key("c-w/20"), rdescript="Browser: Close Tab") * Repeat(extra="n"),
        "new tab [<n>]":                R(Key("c-t"), rdescript="Browser: New Tab") * Repeat(extra="n"),
        "reopen tab [<n>]":             R(Key("cs-t"), rdescript="Browser: Reopen Tab") * Repeat(extra="n"),
        "next tab [<n>]":               R(Key("c-tab"), rdescript="Browser: Next Tab") * Repeat(extra="n"),
        "previous tab [<n>]":           R(Key("cs-tab"), rdescript="Browser: Previous Tab") * Repeat(extra="n"),
        "show history":                 R(Key("c-h"), rdescript="Browser: Show History"),
        "show downloads":               R(Key("c-j"), rdescript="Browser: Show Downloads"),
        "zoom in <n>":                  R(Key("c-plus/20"), rdescript="Browser: Zoom In") * Repeat(extra="n"),
        "zoom out <n>":                 R(Key("c-minus/20"), rdescript="Browser: Zoom") * Repeat(extra="n"),
        "refresh":                      R(Key("c-r"), rdescript="Browser: Refresh"),
        "super refresh":                R(Key("c-f5"), rdescript="Browser: Super Refresh"),
        "[add] bookmark":               R(Key("c-d"), rdescript="Browser: Add Bookmark"),
        
        "developer tools":              R(Key("f12"), rdescript="Browser: Developer Tools"),
        "resume":                       R(Key("f8"), rdescript="Browser: Resume"),
        "step over":                    R(Key("f10"), rdescript="Browser: Step Over"),
        "step into":                    R(Key("f11"), rdescript="Browser: Step Into"), 
        "step out":                     R(Key("s-f11"), rdescript="Browser: Step Out"),
        
        "IRC identify":                 R(Text("/msg NickServ identify PASSWORD"), rdescript="IRC Chat Channel Identify"),
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