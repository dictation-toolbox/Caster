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
                       Key, Text, Function, IntegerRef)
from caster.lib.dfplus.state.short import R

def apply(n):
    if n!=0:
        Text("stash@{"+str(int(n))+"}").execute()

class CommandRule(MappingRule):

    mapping = {
        "initialize repository":       Text( "git init" )+Key("enter"),
        "add":              R(Key("g, i, t, space, a, d, d, space, dot, enter"), rdescript="GIT: Add All"),
        "status":           R(Key( "g, i, t, space, s, t, a, t, u, s, enter" ), rdescript="GIT: Status"),
        "commit":           R(Key( "g, i, t, space, c, o, m, m, i, t, space, minus, a, m, space, apostrophe, apostrophe, left"), rdescript="GIT: Commit"),
        "checkout":         Text( "git checkout " ),
        "merge":            Text( "git merge " ),
        "merge tool":       Text( "git mergetool")+Key("enter"),
        "fetch":            Text( "git fetch" )+Key("enter"),
        
        
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
        "visualize file":   Text("gitk "),
        "visualize all":    Text("gitk --all")+Key("enter"),
        
        "exit":             Text( "exit" )+Key("enter"),
        
        
        
        "stash":            Text("git stash")+Key("enter"),
        "stash apply [<n>]":Text("git stash apply")+Function(apply),
        "stash list":       Text("git stash list")+Key("enter"),
        "stash branch":     Text("git stash branch NAME"),

        "cherry pick":      Text("git cherry-pick "),
        "abort cherry pick":Text("git cherry-pick --abort"),
        
        "GUI":              Text("git gui")+Key("enter"),
        "blame":            Text("git blame PATH -L FIRSTLINE,LASTLINE"),
        "gooey blame":      Text("git gui blame PATH"),
        
        "search recursive": Text("grep -r -i \"PATTERN\" *"),
        "search recursive count": Text("grep -r -i \"PATTERN\" * | wc -l"),
        "search recursive filetype": Text("find . -name \"*.java\" -exec grep -r -i \"PATTERN\" {} \\;"),
        "to file":          Text(" > FILENAME"),
        }
    extras = [
              IntegerRef("n", 1, 50),
             ]
    defaults ={"n": 0}


#---------------------------------------------------------------------------

context = AppContext(executable="sh")
grammar = Grammar("MINGW32", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None