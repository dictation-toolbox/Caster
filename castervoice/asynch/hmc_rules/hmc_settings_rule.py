from dragonfly import Function, MappingRule

from castervoice.asynch.hmc_rules.hmc_support import kill
from castervoice.lib import control, settings
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


def hmc_settings_complete():
    control.nexus().comm.get_com("hmc").complete()


class HMCSettingsRule(MappingRule):
    mapping = {
        "kill homunculus": R(Function(kill)),
        "complete": R(Function(hmc_settings_complete)),
    }


def get_rule():
    details = RuleDetails(name="h m c settings rule",
                          title=settings.SETTINGS_WINDOW_TITLE)
    return HMCSettingsRule, details
