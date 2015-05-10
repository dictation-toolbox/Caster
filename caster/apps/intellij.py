from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, IntegerRef,
                       Key, Text, Repeat, Pause)
from dragonfly.actions.action_mimic import Mimic

 
class CommandRule(MappingRule):

    mapping = {
                    
        "quickfix":                 Key("a-enter"),
        "duplicate":                Key("c-d"),
        "auto complete":            Key("cs-a"),
        "format code":              Key("ca-l"),
        "show doc":                 Key("c-q"),
        "show param":               Key("c-p"),
        "Jen method":               Key("a-insert"),
        "jump to source":           Key("f4"),
        "delete line":              Key("c-y"),
        "search symbol":            Key("cas-n"),
        "build":                    Key("c-f9"),
        "build and run":            Key("s-f10"),
        "next tab":                 Key("a-right"),
        "previous tab":             Key("a-left"),
        
        "comment line":             Key("c-slash"), 
        "uncomment line":           Key("cs-slash"), 
        "select ex":                Key("c-w"), 
        "select ex down":           Key("cs-w"),
        "search everywhere":        Key("shift, shift"), 
        "pop":                      Key("c-space"), 
        "find in current":          Key("cs-f"), 
        
        

        }
    extras = [
              Dictation("text"),
              Dictation("mim"),
              IntegerRef("n", 1, 1000),
              
             ]
    defaults = {"n": 1, "mim":""}

#---------------------------------------------------------------------------

context = AppContext(executable="idea", title="IntelliJ") | AppContext(executable="idea64", title="IntelliJ")
grammar = Grammar("IntelliJ", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None