#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for git

"""


#---------------------------------------------------------------------------

from dragonfly import (Grammar, AppContext, MappingRule,
                       Key, Text)


class CommandRule(MappingRule):

    mapping = {
        "initialize":       Text( "git init" )+Key("enter"),
        "add":              Text( "git add ." )+Key("enter"),
        "status":           Text( "git status" )+Key("enter"),
        "commit":           Text( "git commit -am ''" )+Key("left"),
        "(get push | push)":Text( "git push" )+Key("enter"),
        "pull":             Text( "git pull" )+Key("enter"),
        "CD up":            Text( "cd .." )+Key("enter"),
        "CD":               Text( "cd " ),
        "list":             Text( "ls" )+Key("enter"),
        "make directory":   Text( "mkdir " ),
        "undo [last] commit": Text("git reset --soft HEAD~1")+Key("enter"),
        "visualize":        Text("gitk")+Key("enter"),
        "stop tracking [file]": Text("git rm --cached FILENAME"),
        "exit":             Text( "exit" )+Key("enter"),
        
        # navigation to specific project paths
        "go to simulator":  Text("cd C:/Users/dave/workspace/simulator")+Key("enter"),
        "go to dragonfly":  Text("cd C:/NatLink/NatLink/MacroSystem")+Key("enter"),
        "go to salty":  Text("cd C:/Users/dave/workspace/aptana/saltybot")+Key("enter"),
        
        
        }
    extras = [
              
             ]
    defaults ={}


#---------------------------------------------------------------------------

context = AppContext(executable="sh")
grammar = Grammar("MINGW32", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None