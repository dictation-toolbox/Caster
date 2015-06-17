from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, IntegerRef,
                       Key, Text, Repeat, Pause)
from dragonfly.actions.action_mimic import Mimic

from caster.lib.dfplus.state.short import R


# next tab
class CommandRule(MappingRule):

    mapping = {
                    
            "previous (editor | tab) [<n>]":            R(Key("cs-f6"), rdescript="Eclipse: Previous Tab") * Repeat(extra="n"),  # these two must be set up in the eclipse preferences
            "next (editor | tab) [<n>]":                R(Key("c-f6"), rdescript="Eclipse: Next Tab") * Repeat(extra="n"),
            "close (editor | tab) [<n>]":               R(Key("c-w"), rdescript="Eclipse: Close Tab") * Repeat(extra="n"),
            "open resource":                            R(Key("cs-r"), rdescript="Eclipse: Open Resource"),
            "open type":                                R(Key("cs-t"), rdescript="Eclipse: Open Type"),

            "[go to] line <n> [<mim>]":                 Key("c-l") + Pause("50") + Text("%(n)d") + Key("enter")+ Pause("50")+Mimic(extra="mim"),
            "jump to source":                           R(Key("f3"), rdescript="Eclipse: Jump To Source"),
            "editor select":                            R(Key("c-e"), rdescript="Eclipse: Editor Select"),
            
            "step over [<n>]":                          R(Key("f6/50") * Repeat(extra="n"), rdescript="Eclipse: Step Over"),
            "step into":                                R(Key("f5"), rdescript="Eclipse: Step Into"),
            "step out [of]":                            R(Key("f7"), rdescript="Eclipse: Step Out"),
            "resume":                                   R(Key("f8"), rdescript="Eclipse: Resume"),
            "(debug | run) last":                       R(Key("f11"), rdescript="Eclipse: Run Last"),
            "mark occurrences":                         R(Key("as-o"), rdescript="Eclipse: Mark Occurrences"),

            # "terminate" changes to the settings for this hotkey: (when: in dialogs and windows)
            "terminate":                                R(Key("c-f2"), rdescript="Eclipse: Terminate Running Program"),
            
            "search for this everywhere":               R(Key("ca-g"), rdescript="Eclipse: Search Project"),
            "refractor symbol":                         R(Key("sa-r"), rdescript="Eclipse: Re-Factor Symbol"),
            
            "symbol next [<n>]":                        R(Key("c-k"), rdescript="Eclipse: Symbol Next") * Repeat(extra="n"),
            "symbol prior [<n>]":                       R(Key("cs-k"), rdescript="Eclipse: Symbol Prior") * Repeat(extra="n"),            
            
            "format code":                              R(Key("cs-f"), rdescript="Eclipse: Format Code"),
            "do imports":                               R(Key("cs-o"), rdescript="Eclipse: Do Imports"),
            "comment line":                             R(Key("c-slash"), rdescript="Eclipse: Comment Line"),
            
            "build it":                                 R(Key("c-b"), rdescript="Eclipse: Build"), 
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
