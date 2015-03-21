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
        "merge":            Text( "git merge " ),
        "merge tool":       Text( "git mergetool")+Key("enter"),
        "fetch":            Text( "git fetch" ),
        
        "(get push | push)":Text( "git push" )+Key("enter"),
        "pull":             Text( "git pull" )+Key("enter"),
        "CD up":            Text( "cd .." )+Key("enter"),
        "CD":               Text( "cd " ),
        "list":             Text( "ls" )+Key("enter"),
        "make directory":   Text( "mkdir " ),
        
        "undo [last] commit": Text("git reset --soft HEAD~1")+Key("enter"),
        "undo changes":     Text("git reset --hard")+Key("enter"),
        "stop tracking [file]": Text("git rm --cached FILENAME"),
        "preview remove untracked": Text("git clean -nd")+Key("enter"),
        "remove untracked": Text("git clean -fd")+Key("enter"),
        
        "visualize":        Text("gitk")+Key("enter"),
        
        "exit":             Text( "exit" )+Key("enter"),
        
        "blame":            Text("git blame PATHTOFILE -L FIRSTLINE,LASTLINE"),
        
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