#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for but pycharm

"""


#---------------------------------------------------------------------------

from dragonfly import (Grammar, AppContext, MappingRule,
                       Key, Text)


class CommandRule(MappingRule):

    mapping = {
        "fix this":                 Key("a-enter"),
        "duplicate":                Key("c-d"),
        "auto complete":            Key("cs-a"),
        "format code":              Key("ca-l"),
        "show doc":                 Key("c-q"),
        "show param":               Key("c-p"),
        "Jen method":               Key("a-insert"),
        "jump to source":           Key("f4"),
        "delete line":              Key("c-y"),
        "search symbol":            Key("cas-n"),
        "build":                    Key("c-f9"),
        "build and run":            Key("s-f10"),
        "next tab":                 Key("a-right"),
        "previous tab":             Key("a-left"),
        
        "comment line":             Key("c-slash"), 
        "uncomment line":           Key("cs-slash"), 
        "select ex":                Key("c-w"), 
        "select ex down":           Key("cs-w"),
        "search everywhere":        Key("shift, shift"), 
        "pop":                      Key("c-space"), 
        "find in current":          Key("cs-f"),
        
        }
    extras = []
    defaults = {}


#---------------------------------------------------------------------------

context = AppContext(executable="studio64")
grammar = Grammar("android studio", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
