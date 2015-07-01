from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, IntegerRef,
                       Key, Text, Repeat, Pause)


# next tab
class CommandRule(MappingRule):

    mapping = {
        "go to line":               Key("c-g"),
        "go to symbol":             Key("c-r"), 
        "go to word":               Key("c-semicolon"), 
        
        "next tab":                 Key("c-pageup"), 
        "prior tab":                Key("c-pagedown"),
        
        "transform upper":          Key("control:down, k, u, control:up"), 
        "transform lower":          Key("control:down, k, l, control:up"),
        
        
        "comment line":             Key("c-slash"), 
        "comment block":            Key("cs-slash"), 
        "full screen":              Key("f11"), 
        "set bookmark":             Key("c-f2"), 
        "next bookmark":            Key("f2"), 
        
        "open file":                Key("c-p"), 
        "find next":                Key("f3"), 
        "find prior":               Key("c-f3"), 
        
        
        "search for this everywhere": Key("cs-f"), 

        }
    extras = [
              Dictation("text"),
              Dictation("mim"),
              IntegerRef("n", 1, 1000),
              
             ]
    defaults = {"n": 1, "mim":""}

#---------------------------------------------------------------------------

context = AppContext(executable="sublime_text", title="Sublime Text 2") | AppContext(executable="eclipse", title="Eclipse") | AppContext(executable="AptanaStudio3")
grammar = Grammar("Sublime", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
