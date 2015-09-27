from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, IntegerRef,
                       Key, Text, Repeat, Pause)

from caster.lib import settings
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.state.short import R


# next tab
class CommandRule(MappingRule):

    mapping = {
        "go to line":               R(Key("c-g"), rdescript="Sublime: Go To Line"),
        "go to symbol":             R(Key("c-r"), rdescript="Sublime: Go To Symbol"), 
        "go to word":               R(Key("c-semicolon"), rdescript="Sublime: Go To Word"), 
        
        "next tab":                 R(Key("c-pageup"), rdescript="Sublime: Next Tab"), 
        "prior tab":                R(Key("c-pagedown"), rdescript="Sublime: Prior Tab"),
        
        "transform upper":          R(Key("control:down, k, u, control:up"), rdescript="Sublime: Transform Upper"), 
        "transform lower":          R(Key("control:down, k, l, control:up"), rdescript="Sublime: Transform Lower"),
        
        
        "comment line":             R(Key("c-slash"), rdescript="Sublime: Comment Line"), 
        "comment block":            R(Key("cs-slash"), rdescript="Sublime: Comment Block"), 
        "full screen":              R(Key("f11"), rdescript="Sublime: Fullscreen"), 
        "set bookmark":             R(Key("c-f2"), rdescript="Sublime: Set Bookmark"), 
        "next bookmark":            R(Key("f2"), rdescript="Sublime: Next Bookmark"), 
        
        "open file":                R(Key("c-p"), rdescript="Sublime: Open File"), 
        "find next":                R(Key("f3"), rdescript="Sublime: Find Next"), 
        "find prior":               R(Key("c-f3"), rdescript="Sublime: Find Prior"), 
        
        
        "search for this everywhere": R(Key("cs-f"), rdescript="Sublime: Search Everywhere"), 

        }
    extras = [
              Dictation("text"),
              Dictation("mim"),
              IntegerRefST("n", 1, 1000),
              
             ]
    defaults = {"n": 1, "mim":""}

#---------------------------------------------------------------------------

context = AppContext(executable="sublime_text", title="Sublime Text 2") | AppContext(executable="eclipse", title="Eclipse") | AppContext(executable="AptanaStudio3")
grammar = Grammar("Sublime", context=context)
grammar.add_rule(CommandRule(name="sublime"))
if settings.SETTINGS["apps"]["sublime"]:
    grammar.load()