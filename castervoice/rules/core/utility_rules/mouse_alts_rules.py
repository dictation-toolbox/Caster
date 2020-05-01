from dragonfly import MappingRule, Function, Choice
from castervoice.lib import navigation, utilities
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.short import R


class MouseAlternativesRule(MappingRule):
    mapping = {
        "legion [<monitor>] [<rough>]":
            R(Function(navigation.mouse_alternates, mode="legion") +
                Function(utilities.focus_mousegrid, gridtitle="legiongrid")),
        "rainbow [<monitor>]":
            R(Function(navigation.mouse_alternates, mode="rainbow") +
                Function(utilities.focus_mousegrid, gridtitle="rainbowgrid")),
        "douglas [<monitor>]":
            R(Function(navigation.mouse_alternates, mode="douglas") +
                Function(utilities.focus_mousegrid, gridtitle="douglasgrid")),
        "sudoku [<monitor>]":
            R(Function(navigation.mouse_alternates, mode="sudoku") +
                Function(utilities.focus_mousegrid, gridtitle="sudokugrid")),
    }
    extras = [
        IntegerRefST("monitor", 1, 10),
        Choice("rough", {
            "rough": True,
            "detailed": False
        })
    ]
    defaults = {"rough": True}


def get_rule():
    details = RuleDetails(name="mouse alternatives rule")
    return MouseAlternativesRule, details
