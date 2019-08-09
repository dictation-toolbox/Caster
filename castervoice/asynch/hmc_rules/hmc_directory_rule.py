from dragonfly import Function

from castervoice.lib import control, settings
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


def hmc_directory_browse():
    control.nexus().comm.get_com("hmc").do_action("dir")


class HMCDirectoryRule(MergeRule):
    mapping = {
        # specific to directory browser
        "browse":
            R(Function(hmc_directory_browse))
    }


def get_rule():
    details = RuleDetails(title=settings.HMC_TITLE_DIRECTORY, rdp_mode_exclusion=True)
    return HMCDirectoryRule, details
