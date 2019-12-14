from dragonfly import MappingRule, Playback

from castervoice.lib.actions import Key
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class WindowManagementRule(MappingRule):
    mapping = {
        'minimize':
            R(Playback([(["minimize", "window"], 0.0)])),
        'maximize':
            R(Playback([(["maximize", "window"], 0.0)])),
        "remax":
            R(Key("a-space/10,r/10,a-space/10,x")),
    }


def get_rule():
    details = RuleDetails(name="window management rule")
    return WindowManagementRule, details
