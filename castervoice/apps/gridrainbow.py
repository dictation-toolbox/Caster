"""
Command-module for RainbowGrid

"""

from dragonfly import (Grammar, Function, Playback, Choice, MappingRule)

from castervoice.asynch.mouse import grids
from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R
from castervoice.lib.context import AppContext

_NEXUS = control.nexus()


def kill(nexus):
    nexus.comm.get_com("grids").kill()


def send_input(pre, color, n, action, nexus):
    s = nexus.comm.get_com("grids")
    s.move_mouse(int(pre), int(color), int(n))
    s.kill()
    grids.wait_for_death(settings.RAINBOW_TITLE)
    int_a = int(action)
    if int_a == 0:
        Playback([(["mouse", "left", "click"], 0.0)]).execute()
    elif int_a == 1:
        Playback([(["mouse", "right", "click"], 0.0)]).execute()


class GridControlRule(MergeRule):

    mapping = {
        "[<pre>] <color> <n> [<action>]":
            R(Function(send_input, nexus=_NEXUS), rdescript="Rainbow Grid: Action"),
        "exit | escape | cancel":
            R(Function(kill, nexus=_NEXUS), rdescript="Exit Rainbow Grid"),
    }
    extras = [
        IntegerRefST("pre", 0, 9),
        Choice(
            "color", {
                "red": 0,
                "(orange | tan | brown)": 1,
                "yellow": 2,
                "green": 3,
                "blue": 4,
                "purple": 5
            }),
        Choice("action", {
            "kick": 0,
            "psychic": 1,
        }),
        IntegerRefST("n", 0, 100),
    ]
    defaults = {
        "pre": 0,
        "action": -1,
    }


#---------------------------------------------------------------------------

context = AppContext(title="rainbowgrid")
grammar = Grammar("rainbowgrid", context=context)
if settings.SETTINGS["apps"]["rainbow"]:
    rule = GridControlRule(name="rainbow")
    gfilter.run_on(rule)
    grammar.add_rule(rule)
    grammar.load()
