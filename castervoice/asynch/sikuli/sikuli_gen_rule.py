from dragonfly import MappingRule

from castervoice.asynch.sikuli import sikuli_controller
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.actions2 import NullAction


class SikuliRule(MappingRule):
    """
    The tricky thing about this rule is that its commands must be retrieved from
    the running Sikuli server. So it can't be instantiated properly unless the
    Sikuli server is already running.

    Therefore, it must itself be activated as a side effect of the function
    which starts the Sikuli server.
    """

    def __init__(self, name="sikuli custom"):
        super(SikuliRule, self).__init__(name=name, mapping=self._get_mapping())

    def _get_mapping(self):
        mapping = sikuli_controller.get_instance().generate_commands()
        if len(mapping) == 0:
            mapping["this was a test instantiation"] = NullAction()
        return mapping


def get_rule():
    return SikuliRule, RuleDetails(name="sikuli custom")
