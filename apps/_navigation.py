from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, IntegerRef,Mouse,Playback, 
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
        
        'kick':                         Function(navigation.kick),
        'kick mid':                     Function(navigation.kick_middle),
        'psychic':                         Function(navigation.kick_right),
        '(kick double|double kick)':    Playback([(["mouse", "double", "click"], 0.0)]),
        "shift right click":            Key("shift:down") + Mouse("right") + Key("shift:up"),
        "curse <direction> [<direction2>] [<nnavi500>]":Function(navigation.curse, extra={"direction", "direction2", "nnavi500"}),
        "left point":                   Playback([(["MouseGrid"], 0.1), (["four", "four"], 0.1), (["click"], 0.0)]),
        "right point":                  Playback([(["MouseGrid"], 0.1), (["six", "six"], 0.1), (["click"], 0.0)]),
        "center point":                 Playback([(["MouseGrid"], 0.1), (["click"], 0.0)]),
    
        "colic":                            Key("control:down") + Mouse("left") + Key("control:up"),
        "garb [<nnavi500>]":                Mouse("left")+Mouse("left")+Key("c-c")+Function(navigation.clipboard_to_file, extra="nnavi500"),
        }
    extras = [
              Dictation("text"),
              Dictation("mim"),
              IntegerRef("n", 1, 50),
              IntegerRef("nnavi500", 1, 500),
              Choice("direction3",
                {"out": "right", "back out": "left", "next": "right", "previous": "left"
                }),
              Choice("direction",
                {"up": "up", "down": "down", "left": "left", "right": "right",
                }),
              Choice("direction2",
                {"right": "right", "up": "up", "down": "down", "left": "left", 
                }),
              navigation.TARGET_CHOICE
              
             ]
    defaults = {"n": 1, "mim":"", "nnavi500": 1, "direction2":""}

#---------------------------------------------------------------------------

context = AppContext(executable="javaw", title="Eclipse") | AppContext(executable="AptanaStudio3")
grammar = Grammar("_navigation", context=None)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
