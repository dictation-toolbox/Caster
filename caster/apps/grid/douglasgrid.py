"""
Command-module for DouglasGrid

"""

import time

from dragonfly import (Grammar, AppContext, Function,
                       IntegerRef, Repeat, Playback,
                       Key, Choice, MappingRule)
from caster.lib.dfplus.state.short import R

from caster.asynch.mouse import grids
from caster.lib import settings, control


def kill():
    control.COMM.get_com("grids").kill()

def send_input(n, n2, action):
    s = control.COMM.get_com("grids")
    s.move_mouse(int(n), int(n2))
    s.kill()
    grids.wait_for_death(settings.DOUGLAS_TITLE)
    int_a = int(action)
    if int_a == 0:
        Playback([(["mouse", "left", "click"], 0.0)])._execute()
    elif int_a == 1:
        Playback([(["mouse", "right", "click"], 0.0)])._execute()

class GridControlRule(MappingRule):

    mapping = {
        "<n> [by] <n2> [<action>]":         R(Function(send_input), rdescript="Douglas Grid: Action"),
        "exit":                             R(Function(kill), rdescript="Exit Douglas Grid"),
                }
    extras = [
              IntegerRef("n", 0, 300),
              IntegerRef("n2", 0, 300),
              Choice("action", {
                              "kick": 0,
                              "psychic": 1,
                             }
                    ),
             ]
    defaults = {
            "action": -1,
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
