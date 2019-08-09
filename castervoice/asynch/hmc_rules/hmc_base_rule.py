from dragonfly import Function

from castervoice.asynch.hmc_rules.hmc_support import kill
from castervoice.lib import control, settings
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


def complete():
    control.nexus().comm.get_com("hmc").complete()


class HMCRule(MergeRule):
    mapping = {
        "kill homunculus":
            R(Function(kill)),
        "complete":
            R(Function(complete))
    }


def get_rule():
    details = RuleDetails(title=settings.HOMUNCULUS_VERSION, rdp_mode_exclusion=True)
    return HMCRule, details
