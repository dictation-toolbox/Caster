from dragonfly import Function, MappingRule

from castervoice.asynch.hmc_rules.hmc_support import kill
from castervoice.lib import control, settings
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


def complete():
    control.nexus().comm.get_com("hmc").complete()


class HMCRule(MappingRule):
    mapping = {
        "kill homunculus":
            R(Function(kill)),
        "complete":
            R(Function(complete))
    }


def get_rule():
    details = RuleDetails(name="h m c rule",
                          title=settings.HOMUNCULUS_VERSION)
    return HMCRule, details
