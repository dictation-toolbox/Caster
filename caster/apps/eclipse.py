from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, IntegerRef,
                       Key, Text, Repeat, Pause)
from dragonfly.actions.action_mimic import Mimic
from caster.lib.dfplus.state import R
# next tab
class CommandRule(MappingRule):

    mapping = {
                    
            "previous (editor | tab) [<n>]":            Key("cs-f6") * Repeat(extra="n"),  # these two must be set up in the eclipse preferences
            "next (editor | tab) [<n>]":                Key("c-f6") * Repeat(extra="n"),
            "close (editor | tab) [<n>]":               Key("c-w") * Repeat(extra="n"),
            "open resource":                            R(Key("cs-r"), rdescript="Eclipse: Open Resource"),
            "open type":                                Key("cs-t"),

            "[go to] line <n> [<mim>]":                 Key("c-l") + Pause("50") + Text("%(n)d") + Key("enter")+ Pause("50")+Mimic(extra="mim"),
            "jump to source":                           Key("f3"),
            "editor select":                            Key("c-e"),
            
            "step over [<n>]":                          Key("f6/50") * Repeat(extra="n"),
            "step into":                                Key("f5"),
            "step out [of]":                            Key("f7"),
            "resume":                                   Key("f8"),
            "(debug | run) last":                       Key("f11"),
            "mark occurrences":                         Key("as-o"),

            # "terminate" changes to the settings for this hotkey: (when: in dialogs and windows)
            "terminate":                                R(Key("c-f2"), rdescript="Eclipse: Terminate Running Program"),
            
            "search for this everywhere":               R(Key("ca-g"), rdescript="Eclipse: Search Project"),
            "refractor symbol":                         R(Key("sa-r"), rdescript="Eclipse: Re-Factor Symbol"),
            
            "symbol next [<n>]":                        R(Key("c-k"), rdescript="Eclipse: Symbol Next") * Repeat(extra="n"),
            "symbol prior [<n>]":                       R(Key("cs-k"), rdescript="Eclipse: Symbol Prior") * Repeat(extra="n"),            
            
            "format code":                              R(Key("cs-f"), rdescript="Eclipse: Format Code"),
            "do imports":                               R(Key("cs-o"), rdescript="Eclipse: Do Imports"),
            "comment line":                             R(Key("c-slash"), rdescript="Eclipse: Comment Line"),
            
            
            # requires quick bookmarks plug-in:
#             "set mark [<n>]":                           Key("a-%(n)d"),
#             "go mark [<n>]":                            Key("as-%(n)d"),
        }
    extras = [
              Dictation("text"),
              Dictation("mim"),
              IntegerRef("n", 1, 1000),
              
             ]
    defaults = {"n": 1, "mim":""}

#---------------------------------------------------------------------------

context = AppContext(executable="javaw", title="Eclipse") | AppContext(executable="eclipse", title="Eclipse") | AppContext(executable="AptanaStudio3")
grammar = Grammar("Eclipse", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
