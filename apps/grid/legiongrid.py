"""
Command-module for Legion

"""


import time

from dragonfly import (Grammar, AppContext, Function,
                       IntegerRef, Repeat, Playback,
                       Key, Choice, MappingRule)
import win32api
import win32con

from asynch.mouse import legion
from lib import navigation


def kill():
    legion.communicate().kill()

def send_input(n, action):
    s = legion.communicate()
    
    int_a = int(action)
    response = None
    
    if int_a != 2:
        s.go(str(n))
    elif int_a == 2:
        response = s.retrieve_data_for_highlight(str(int(n)))
    
    s.kill()
    time.sleep(0.1)
    
    if int_a == 0:
        Playback([(["mouse", "left", "click"], 0.0)])._execute()
    elif int_a == 1:
        Playback([(["mouse", "right", "click"], 0.0)])._execute()
    elif int_a == 2:
        x1 = response["l"]
        x2 = response["r"]
        y = response["y"]
        
        win32api.SetCursorPos((x1, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x1, y, 0, 0)
        win32api.SetCursorPos((x2, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x2, y, 0, 0)


class GridControlRule(MappingRule):

    mapping = {
        "<n> [<action>]":                   Function(send_input, extra={"n", "action"}),
        "refresh":                          Function(navigation.mouse_alternates, mode="legion"),
        "exit":                             Key("x") * Repeat(2),


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
