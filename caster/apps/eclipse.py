from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, IntegerRef,
                       Key, Text, Repeat, Pause)
from dragonfly.actions.action_mimic import Mimic

# next tab
class CommandRule(MappingRule):

    mapping = {
                    
            "previous (editor | tab) [<n>]":            Key("cs-f6") * Repeat(extra="n"),  # these two must be set up in the eclipse preferences
            "next (editor | tab) [<n>]":                Key("c-f6") * Repeat(extra="n"),
            "close (editor | tab) [<n>]":               Key("c-w") * Repeat(extra="n"),
            "open resource":                            Key("cs-r"),
            "open type":                                Key("cs-t"),

            "[go to] line <n> [<mim>]":                 Key("c-l") + Pause("50") + Text("%(n)d") + Key("enter")+ Pause("50")+Mimic(extra="mim"),
            "jump to source":                           Key("f3"),
            "editor select":                            Key("c-e"),
            "pop":                                      Key("c-space, down, up"),
            
            "step over [<n>]":                          Key("f6/50") * Repeat(extra="n"),
            "step into":                                Key("f5"),
            "step out [of]":                            Key("f7"),
            "resume":                                   Key("f8"),
            "(debug | run) last":                       Key("f11"),
            "mark occurrences":                         Key("as-o"),

            # "terminate" changes to the settings for this hotkey: (when: in dialogs and windows)
            "terminate":                                Key("c-f2"),
            
            "search for this everywhere":               Key("ca-g"),
            "refractor symbol":                         Key("sa-r"),
            
            "symbol next [<n>]":                        Key("c-k") * Repeat(extra="n"),
            "symbol prior [<n>]":                       Key("cs-k") * Repeat(extra="n"),            
            
            "format code":                              Key("cs-f"),
            "do imports":                               Key("cs-o"),
            "comment line":                             Key("c-slash"),
            
            "open resource":                            Key("cs-r"),
            
            
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
