from dragonfly import (Grammar, AppContext, Dictation, Key, Text)

from caster.lib import control
from caster.lib import settings
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


class SublimeRule(MergeRule):
    pronunciation = "sublime"

    mapping = {
        "[go to] line <n>":         R(Key("c-g") + Text("%(n)s") + Key("enter"), rdescript="Sublime: Go to Line #"),
        "go to symbol":             R(Key("c-r"), rdescript="Sublime: Go To Symbol"), 
        "go to word":               R(Key("c-semicolon"), rdescript="Sublime: Go To Word"), 
        
        "transform upper":          R(Key("control:down, k, u, control:up"), rdescript="Sublime: Transform Upper"), 
        "transform lower":          R(Key("control:down, k, l, control:up"), rdescript="Sublime: Transform Lower"),
        
        "comment line":             R(Key("c-slash"), rdescript="Sublime: Comment Line"), 
        "comment block":            R(Key("cs-slash"), rdescript="Sublime: Comment Block"), 
        "full screen":              R(Key("f11"), rdescript="Sublime: Fullscreen"), 
        "set bookmark":             R(Key("c-f2"), rdescript="Sublime: Set Bookmark"), 
        "next bookmark":            R(Key("f2"), rdescript="Sublime: Next Bookmark"), 
        
        "open file":                R(Key("c-p"), rdescript="Sublime: Open File"), 

        }
    extras = [
              Dictation("text"),
              Dictation("mim"),
              IntegerRefST("n", 1, 1000),
              
             ]
    defaults = {"n": 1, "mim":""}

#---------------------------------------------------------------------------

context = AppContext(executable="sublime_text")
grammar = Grammar("Sublime", context=context)

if settings.SETTINGS["apps"]["sublime"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(SublimeRule())
    else:
        rule = SublimeRule(name="sublime")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()