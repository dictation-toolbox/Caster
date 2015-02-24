from dragonfly import (Function, Text, Grammar, 
                       IntegerRef, Dictation, MappingRule)
    
class ElementUsageRule(MappingRule):
    mapping = {
    "placeholder":                  Text("placeholder"),
    
    }   
    extras = [
              IntegerRef("n", 1, 200),
              IntegerRef("n2", 1, 100),
              Dictation("text"),
             ]
    defaults = {"n": 1, "n2": 1,
               "text": "",
               }

eur=ElementUsageRule()

grammar = Grammar('elementview')
grammar.add_rule(eur)
grammar.load()