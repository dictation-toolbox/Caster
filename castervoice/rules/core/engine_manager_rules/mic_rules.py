from dragonfly import Dictation, MappingRule, Choice, Function
from castervoice.lib.actions import Text

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

from castervoice.lib.ctrl.mgr.engine_manager import EngineModesManager

class CasterMicRule(MappingRule):
    mapping = {
        "caster <mic_mode>": Function(lambda mic_mode: EngineModesManager.set_mic_mode(mode=mic_mode)),     
    }
    extras = [
        Choice(
            "mic_mode", {
                "off": "off",
                "on": "on",
                "sleep": "sleeping",
            }),
    ]
    defaults = {}

def get_rule():
    return CasterMicRule, RuleDetails(name="caster mic mode", transformer_exclusion=True)