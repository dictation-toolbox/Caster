"""
Command-module for Legion

"""

import time

from dragonfly import (Grammar, AppContext, Function, Playback, Choice, MappingRule)
import win32api
import win32con

from caster.lib.asynch.mouse import grids
from caster.lib import control
from caster.lib import navigation, settings
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R

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
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x1, y, 0, 0)
        time.sleep(0.5)
        win32api.SetCursorPos((x2, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x2, y, 0, 0)


class GridControlRule(MergeRule):

    mapping = {
        "<n> [<action>]":
            R(Function(send_input, nexus=_NEXUS), rdescript="Legion: Action"),
        "refresh":
            R(Function(navigation.mouse_alternates, mode="legion", nexus=_NEXUS),
              rdescript="Legion: Refresh"),
        "exit | escape | cancel":
            R(Function(kill, nexus=_NEXUS), rdescript="Exit Legion"),
    }
    extras = [
        Choice("action", {
            "kick": 0,
            "psychic": 1,
            "light": 2,
        }),
        IntegerRefST("n", 0, 1000),
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
