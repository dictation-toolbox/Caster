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
                       Dictation, Playback, IntegerRef, Function,
                       Key, Text, Repeat, WaitWindow, Mouse, Pause)

def save_image(dict, n):
    s=str(dict)
    Mouse("right")._execute()
    Pause("40")._execute()
    Key("up/10:5")._execute()
    Key("enter")._execute()
    Key("c-tab")._execute()
    Key("c-s")._execute()
    if not s=="nothing":
        n=str(int(n))
        Pause("40")._execute()
        Text((s[0]+n+"_"))._execute()
    

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
        "search for <dict>":            Key("c-t")+WaitWindow(title="New Tab")+ Text("%(dict)s"),
        "git hub":                      Text("github"),
        "save image [<dict> <n>]":      Function(save_image, extra={"dict", "n"}),
        "developer tools":              Key("f12"),
        "[add] bookmark":               Key("c-d"),
        }
    extras = [
              Dictation("dict"),
              IntegerRef("n",1, 100),
             ]
    defaults ={"n": 1, "dict":"nothing"}


#---------------------------------------------------------------------------

context = AppContext(executable="chrome")
grammar = Grammar("Google Chrome", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None