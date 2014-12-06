"""
Command-module for Legion

"""

import time

from dragonfly import (Grammar, AppContext, Function,
                       IntegerRef, Repeat, Playback,
                       Key, Choice, MappingRule)

from lib import utilities


def send_input(color, n, action):
    Key(str(color))._execute()    
    if int(n) < 10:
        utilities.press_digits(0)
    utilities.press_digits(n)
    int_a = int(action)
    if int_a != -1:
        for i in range(0, 2):
            Key("x")._execute()
        time.sleep(0.1)
        if int_a==0:
            Playback([(["mouse", "left", "click"], 0.0)])._execute()
        elif int_a==1:
            Playback([(["mouse", "right", "click"], 0.0)])._execute()


class GridControlRule(MappingRule):

    mapping = {
        "<color> <n> [<action>]":           Function(send_input, extra={"color", "n", "action"}),
        "refresh":                          Key("r"),
        "exit":                             Key("x") * Repeat(2),


        }
    extras = [
              Choice("color", {
                              "red": "t",
                              "green": "e",
                             }
                    ),
              Choice("action", {
                              "kick": "0",
                              "psychic": "1",
                             }
                    ),
              IntegerRef("n", 0, 1000),
              
             ]
    defaults = {
            "action": "-1",
            }

#---------------------------------------------------------------------------

context = AppContext(title="legiongrid")
grammar = Grammar("legiongrid", context=context)
grammar.add_rule(GridControlRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
