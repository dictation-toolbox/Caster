from dragonfly import MappingRule, Choice, Function
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails

from castervoice.lib import control


def _set_mode(mic_mode):
    control.nexus().engine_modes_manager.set_mic_mode(mode=mic_mode)


class CasterMicRule(MappingRule):
    mapping = {
        "caster <mic_mode>": Function(lambda mic_mode: _set_mode(mic_mode)),
    }
    extras = [
        Choice("mic_mode", {
            "off": "off",
            "on": "on",
            "sleep": "sleeping",
        }),
    ]
    defaults = {}


def get_rule():
    return CasterMicRule, RuleDetails(name="caster mic modes")