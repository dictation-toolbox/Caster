from dragonfly import MappingRule

from castervoice.asynch.sikuli import sikuli_controller
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails

_CONTROLLER = sikuli_controller.get_instance()


class SikuliRule(MappingRule):

    def __init__(self):
        super(SikuliRule, self).__init__(name="sikuli custom",
                                         mapping=_CONTROLLER.generate_commands())


def get_rule():
    return SikuliRule, RuleDetails(name="sikuli custom")
