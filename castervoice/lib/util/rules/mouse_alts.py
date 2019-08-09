from dragonfly import MappingRule, Function

from castervoice.lib import navigation
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.short import R


class MouseAlternativesRule(MappingRule):
    mapping = {
        "legion [<monitor>]":
            R(Function(navigation.mouse_alternates, mode="legion")),
        "rainbow [<monitor>]":
            R(Function(navigation.mouse_alternates, mode="rainbow")),
        "douglas [<monitor>]":
            R(Function(navigation.mouse_alternates, mode="douglas")),
    }
    extras = [
        IntegerRefST("monitor", 1, 10)
    ]
    defaults = {}


def get_rule():
    details = RuleDetails(name="mouse alternatives rule",
                          rdp_mode_exclusion=True)
    return MouseAlternativesRule, details
