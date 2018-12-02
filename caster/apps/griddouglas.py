"""
Command-module for DouglasGrid

"""
from dragonfly import (Grammar, AppContext, Function, Playback, Choice, MappingRule)

from caster.lib.asynch.mouse import grids
from caster.lib import control
from caster.lib import settings
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R

_NEXUS = control.nexus()


def kill(nexus):
    nexus.comm.get_com("grids").kill()


def send_input(n, n2, action, nexus):
    s = nexus.comm.get_com("grids")
    s.move_mouse(int(n), int(n2))
    s.kill()
    grids.wait_for_death(settings.DOUGLAS_TITLE)
    int_a = int(action)
    if int_a == 0:
        Playback([(["mouse", "left", "click"], 0.0)]).execute()
    elif int_a == 1:
        Playback([(["mouse", "right", "click"], 0.0)]).execute()


class GridControlRule(MergeRule):

    mapping = {
        "<n> [by] <n2> [<action>]":
            R(Function(send_input, nexus=_NEXUS), rdescript="Douglas Grid: Action"),
        "exit | escape | cancel":
            R(Function(kill, nexus=_NEXUS), rdescript="Exit Douglas Grid"),
    }
    extras = [
        IntegerRefST("n", 0, 300),
        IntegerRefST("n2", 0, 300),
        Choice("action", {
            "kick": 0,
            "psychic": 1,
        }),
    ]
    defaults = {
        "action": -1,
    }


#---------------------------------------------------------------------------

context = AppContext(title="douglasgrid")
grammar = Grammar("douglasgrid", context=context)

if settings.SETTINGS["apps"]["douglas"]:
    rule = GridControlRule(name="Douglas")
    gfilter.run_on(rule)
    grammar.add_rule(rule)
    grammar.load()
