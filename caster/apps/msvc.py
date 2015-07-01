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
        
           
            "cursor prior":                             Key("c-minus"), 
            "cursor next":                              Key("cs-minus"), 
            "toggle fullscreen":                        Key("sa-enter"), 
            "resolve":                                  Key("c-dot"), 
            "jump to source":                           Key("f12"), 
            "snippet":                                  Key("tab"), 
            "search for this everywhere":               Key("cs-f"), 
             
            "step over [<n>]":                          Key("f10/50") * Repeat(extra="n"),
            "step into":                                Key("f11"),
            "step out [of]":                            Key("s-f11"),
            "resume":                                   Key("f8"),
            "build [last]":                             Key("ca-f7"),
            "debug [last]":                             Key("f5"),
            "comment out":                              Key("c-k/50, c-c"),
            "on comment out":                           Key("c-k/50, c-u"),
            
            "set bookmark":                             Key("c-k, c-k"), 
            "next bookmark":                            Key("c-k, c-n"), 
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

context = AppContext(executable="WDExpress")
grammar = Grammar("WDExpress", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
