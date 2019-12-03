from dragonfly import Function, MappingRule

from castervoice.lib import utilities
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class WindowsSpeechRecognitionRule(MappingRule):

    mapping = {
        "reboot windows speech recognition":
            R(Function(utilities.reboot, wsr=True)),
    }
    extras = []
    defaults = {}


def get_rule():
    return WindowsSpeechRecognitionRule, RuleDetails(name="w s r")
