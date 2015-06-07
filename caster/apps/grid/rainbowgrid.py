"""
Command-module for RainbowGrid

"""


from dragonfly import (Grammar, AppContext, Function,
                       IntegerRef, Repeat, Playback,
                       Key, Choice, MappingRule)

from caster.asynch.mouse import grids
from caster.lib import settings, control
from caster.lib.dfplus.state.short import R

def kill():
    control.COMM.get_com("grids").kill()

def send_input(pre, color, n, action):
    s=control.COMM.get_com("grids")
    s.move_mouse(int(pre), int(color), int(n))
    s.kill()
    grids.wait_for_death(settings.RAINBOW_TITLE)
    int_a = int(action)
    if int_a == 0:
        Playback([(["mouse", "left", "click"], 0.0)])._execute()
    elif int_a == 1:
        Playback([(["mouse", "right", "click"], 0.0)])._execute()


class GridControlRule(MappingRule):

    mapping = {
        "[<pre>] <color> <n> [<action>]":   R(Function(send_input), rdescript="Rainbow Grid: Action"),
        "exit":                             R(Function(kill), rdescript="Exit Rainbow Grid"),


        }
    extras = [
              IntegerRef("pre", 0, 9),
              Choice("color", {
                              "red": 0,
                              "(orange | tan | brown)": 1,
                              "yellow": 2,
                              "green": 3,
                              "blue": 4,
                              "purple": 5
                             }
                    ),
              Choice("action", {
                              "kick": 0,
                              "psychic": 1,
                             }
                    ),
              IntegerRef("n", 0, 100),
              
             ]
    defaults = {
            "pre": 0,
            "action": -1,
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
