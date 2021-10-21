from dragonfly import MappingRule, Function, Dictation
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib import control


def _dictation_sink_controller():
    micmode = control.nexus().engine_modes_manager.get_mic_mode()
    if micmode == "sleeping":
        return True


class DictationSinkRule(MappingRule):
    mapping = {
        "<text>": Function(lambda text: False),
    }
    extras = [
        Dictation("text"),
    ]
    defaults = {
        "text": "",
    }


def get_rule():
        return DictationSinkRule, RuleDetails(name="dictation sink rule", function_context=_dictation_sink_controller)
