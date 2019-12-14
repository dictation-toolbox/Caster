from dragonfly import MappingRule

from castervoice.lib.actions import Key
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class MatlabNon(MappingRule):
    mapping = {
        "section": R(Key("percent, percent, enter")),
    }


def get_rule():
    return MatlabNon, RuleDetails(name="matlab companion")
