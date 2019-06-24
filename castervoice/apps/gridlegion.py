"""
Command-module for Legion

"""

import time

from dragonfly import (Grammar, Function, Playback, Choice, MappingRule)
import win32api
import win32con

from castervoice.asynch.mouse import grids
from castervoice.lib import control
from castervoice.lib import navigation, settings
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R
from castervoice.lib.context import AppContext

_NEXUS = control.nexus()


def kill(nexus):
    nexus.comm.get_com("grids").kill()


def send_input(n, action, nexus):
    s = nexus.comm.get_com("grids")

    int_a = int(action)
    response = None

    if int_a != 2:
        s.go(str(n))
    elif int_a == 2:
        response = s.retrieve_data_for_highlight(str(int(n)))

    s.kill()
    grids.wait_for_death(settings.LEGION_TITLE)

    if int_a == 0:
        Playback([(["mouse", "left", "click"], 0.0)]).execute()
    elif int_a == 1:
        Playback([(["mouse", "right", "click"], 0.0)]).execute()
    elif int_a == 2:
        x1 = response["l"] + 2
        x2 = response["r"]
        y = response["y"]

        win32api.SetCursorPos((x1, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        win32api.SetCursorPos((x2, y))
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def drag_highlight(n1, n2, nexus):
    s = nexus.comm.get_com("grids")

    response1 = s.retrieve_data_for_highlight(str(int(n1)))
    response2 = s.retrieve_data_for_highlight(str(int(n2)))

    s.kill()
    grids.wait_for_death(settings.LEGION_TITLE)

    x11 = response1["l"] + 2
    x12 = response1["r"]
    y1 = response1["y"]
    x21 = response2["l"] + 2
    x22 = response2["r"]
    y2 = response2["y"]
    
    win32api.SetCursorPos((x11, y1))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.SetCursorPos((x22, y2))
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


class GridControlRule(MergeRule):

    mapping = {
        "<n> [<action>]":
            R(Function(send_input, nexus=_NEXUS), rdescript="Legion: Action"),
        "refresh":
            R(Function(navigation.mouse_alternates, mode="legion", nexus=_NEXUS),
              rdescript="Legion: Refresh"),
        "exit | escape | cancel":
            R(Function(kill, nexus=_NEXUS), rdescript="Legion: Exit Legion"),
        "<n1> (select | light) <n2>":
            R(Function(drag_highlight, nexus=_NEXUS), rdescript="Legion: Highlight Between Two Words"),
    }
    extras = [
        Choice("action", {
            "kick": 0,
            "psychic": 1,
            "select | light": 2,
        }),
        IntegerRefST("n", 0, 1000),
        IntegerRefST("n1", 0, 1000),
        IntegerRefST("n2", 0, 1000),
    ]
    defaults = {
        "action": -1,
    }


#---------------------------------------------------------------------------

context = AppContext(title="legiongrid")
grammar = Grammar("legiongrid", context=context)

if settings.SETTINGS["apps"]["legion"]:
    rule = GridControlRule(name="legion")
    gfilter.run_on(rule)
    grammar.add_rule(rule)
    grammar.load()
