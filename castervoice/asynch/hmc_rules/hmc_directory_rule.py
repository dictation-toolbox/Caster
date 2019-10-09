from dragonfly import Function, MappingRule

from castervoice.lib import control, settings
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


def hmc_directory_browse():
    control.nexus().comm.get_com("hmc").do_action("dir")


class HMCDirectoryRule(MappingRule):
    mapping = {
        # specific to directory browser
        "browse":
            R(Function(hmc_directory_browse))
    }


def get_rule():
    details = RuleDetails(name="h m c directory rule",
                          title=settings.HMC_TITLE_DIRECTORY)
    return HMCDirectoryRule, details
