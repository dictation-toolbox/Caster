"""
Command-module for DouglasGrid

"""

import time

from dragonfly import (Grammar, AppContext, Function,
                       IntegerRef, Repeat, Playback,
                       Key, Choice, MappingRule)

from lib import navigation
from lib import utilities


def send_input(n, n2, action):
    if int(n) < 10:
        utilities.press_digits(0)
    utilities.press_digits(n)
    Key("b")._execute()
    if int(n2) < 10:
        utilities.press_digits(0)
    utilities.press_digits(n2)
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
        "<n> [by] <n2> [<action>]":         Function(send_input, extra={"n", "n2", "action"}),
        "exit":                             Key("x") * Repeat(2),


        }
    extras = [
              IntegerRef("n", 0, 300),
              IntegerRef("n2", 0, 300),
              Choice("action", {
                              "kick": "0",
                              "psychic": "1",
                             }
                    ),
             ]
    defaults = {
            "action": "-1",
            }

#---------------------------------------------------------------------------

context = AppContext(title="douglasgrid")
grammar = Grammar("douglasgrid", context=context)
grammar.add_rule(GridControlRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
