"""
Command-module for Legion

"""


import time

from dragonfly import (Grammar, AppContext, Function,
                       IntegerRef, Repeat, Playback,
                       Key, Choice, MappingRule)
import win32api
import win32con

from asynch import legion
from lib import utilities, navigation, settings


def press_keys(color, n):
    Key(str(color))._execute()    
    if int(n) < 10:
        utilities.press_digits(0)
    utilities.press_digits(n)
    for i in range(0, 2):
        Key("x")._execute()
    time.sleep(0.1)

def send_input(color, n, action):
    int_a = int(action)
    if int_a != -1:
        if int_a == 0:
            press_keys(color, n)
            Playback([(["mouse", "left", "click"], 0.0)])._execute()
        elif int_a == 1:
            press_keys(color, n)
            Playback([(["mouse", "right", "click"], 0.0)])._execute()
        elif int_a == 2:
            response=legion.communicate().retrieve_data_for_highlight(str(int(n)))
            x1=response["l"]
            x2=response["r"]
            y=response["y"]
            time.sleep(0.1)
            win32api.SetCursorPos((x1,y))
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x1,y,0,0)
            win32api.SetCursorPos((x2,y))
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x2,y,0,0)


class GridControlRule(MappingRule):

    mapping = {
        "<color> <n> [<action>]":           Function(send_input, extra={"color", "n", "action"}),
        "refresh":                          Function(navigation.mouse_alternates, mode="legion"),
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
                              "light": "2",
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
