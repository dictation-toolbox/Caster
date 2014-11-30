"""
Command-module for RainbowGrid

"""

import time

from dragonfly import (Grammar, AppContext, Function,
                       IntegerRef, Repeat, Playback,
                       Key, Choice, MappingRule)

from lib import utilities, navigation


def send_input(pre, color, n, action):
    Key("p")._execute()
    utilities.press_digits(0)
    utilities.press_digits(pre)
    Key("c")._execute()
    utilities.press_digits(0)
    utilities.press_digits(color)
    Key("n")._execute()
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
        "[<pre>] <color> <n> [<action>]":   Function(send_input, extra={"pre", "color", "n", "action"}),
        "exit":                             Key("x") * Repeat(2),


        }
    extras = [
              IntegerRef("pre", 0, 9),
              Choice("color", {
                              "red": "0",
                              "(orange | tan | brown)": "1",
                              "yellow": "2",
                              "green": "3",
                              "blue": "4",
                              "purple": "5"
                             }
                    ),
              Choice("action", {
                              "kick": "0",
                              "psychic": "1",
                             }
                    ),
              IntegerRef("n", 0, 100),
              
             ]
    defaults = {
            "pre": 0,
            "action": "-1",
            }

#---------------------------------------------------------------------------

context = AppContext(title="rainbowgrid")
grammar = Grammar("rainbowgrid", context=context)
grammar.add_rule(GridControlRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
