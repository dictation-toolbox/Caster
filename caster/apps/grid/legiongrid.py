"""
Command-module for Legion

"""


import time

from dragonfly import (Grammar, AppContext, Function,
                       IntegerRef, Playback,
                       Choice, MappingRule)
import win32api
import win32con

from caster.asynch.mouse import grids
from caster.lib import navigation, settings, control
from caster.lib.dfplus.state.short import R

def kill():
    control.COMM.get_com("grids").kill()

def send_input(n, action):
    s = control.COMM.get_com("grids")
    
    int_a = int(action)
    response = None
    
    if int_a != 2:
        s.go(str(n))
    elif int_a == 2:
        response = s.retrieve_data_for_highlight(str(int(n)))
    
    s.kill()
    grids.wait_for_death(settings.LEGION_TITLE)
    
    if int_a == 0:
        Playback([(["mouse", "left", "click"], 0.0)])._execute()
    elif int_a == 1:
        Playback([(["mouse", "right", "click"], 0.0)])._execute()
    elif int_a == 2:
        x1 = response["l"]+2
        x2 = response["r"]
        y = response["y"]
        
        win32api.SetCursorPos((x1, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x1, y, 0, 0)
        time.sleep(0.5)
        win32api.SetCursorPos((x2, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x2, y, 0, 0)


class GridControlRule(MappingRule):

    mapping = {
        "<n> [<action>]":                   R(Function(send_input), rdescript="Legion: Action"),
        "refresh":                          R(Function(navigation.mouse_alternates, mode="legion"), rdescript="Legion: Refresh"),
        "exit":                             R(Function(kill), rdescript="Exit Legion"),


        }
    extras = [
              Choice("action", {
                              "kick": 0,
                              "psychic": 1,
                              "light": 2,
                             }
                    ),
              IntegerRef("n", 0, 1000),
              
             ]
    defaults = {
            "action":-1,
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
