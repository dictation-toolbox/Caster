from dragonfly import Function

from castervoice.asynch.hmc_rules.hmc_support import kill
from castervoice.lib import control, settings
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


def hmc_settings_complete():
    control.nexus().comm.get_com("hmc").complete()


class HMCSettingsRule(MergeRule):
    mapping = {
        "kill homunculus": R(Function(kill)),
        "complete": R(Function(hmc_settings_complete)),
    }


def get_rule():
    details = RuleDetails(title=settings.SETTINGS_WINDOW_TITLE, rdp_mode_exclusion=True)
    return HMCSettingsRule, details
