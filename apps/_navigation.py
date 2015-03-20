from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, IntegerRef,
                       Key, Choice, Function, Repeat)

from lib import context, navigation


# navigation commands which do not belong in ccr
####################################################################################################
####################################################################################################
####################################################################################################
class CommandRule(MappingRule):

    mapping = {
        "gopher <direction3> <target>":     Function(context.navigate_to_character, extra={"direction3","target"}),    
        "erase multi clipboard":            Function(navigation.erase_multi_clipboard),
        "(F to | F2)":                      Key("f2"),
        "(F six | F6)":                     Key("f6"),
        "(F nine | F9)":                    Key("f9"),
        "de Gaulle [<n>]":                  Key("c-z") * Repeat(extra="n"),


        }
    extras = [
              Dictation("text"),
              Dictation("mim"),
              IntegerRef("n", 1, 50),
              Choice("direction3",
                {"out": "right", "back out": "left", "next": "right", "previous": "left"
                }),
              navigation.TARGET_CHOICE
              
             ]
    defaults = {"n": 1, "mim":""}

#---------------------------------------------------------------------------

context = AppContext(executable="javaw", title="Eclipse") | AppContext(executable="AptanaStudio3")
grammar = Grammar("_navigation", context=None)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
