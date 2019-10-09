from dragonfly import Function, MappingRule

from castervoice.lib import control, settings
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


def hmc_confirm(value):
    control.nexus().comm.get_com("hmc").do_action(value)


class HMCConfirmRule(MappingRule):
    mapping = {
        # specific to confirm
        "confirm":
            R(Function(hmc_confirm, value=True)),
        "disconfirm":
            R(Function(hmc_confirm, value=False),
              rspec="hmc_cancel")
    }


def get_rule():
    details = RuleDetails(name="h m c confirm rule",
                          title=settings.HMC_TITLE_CONFIRM)
    return HMCConfirmRule, details
