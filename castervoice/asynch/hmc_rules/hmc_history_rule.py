from dragonfly import Function, MappingRule, ShortIntegerRef

from castervoice.lib import control, settings
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


def hmc_recording_exclude(n):
    control.nexus().comm.get_com("hmc").do_action("exclude", int(n))


def hmc_recording_repeatable():
    control.nexus().comm.get_com("hmc").do_action("repeatable")


def hmc_recording_check_range(n, n2):
    control.nexus().comm.get_com("hmc").do_action("check_range", [int(n), int(n2)])


def hmc_checkbox(n):
    # can easily check multiple boxes, use a comma-separated list of numbers instead of str(n)
    control.nexus().comm.get_com("hmc").do_action("check", [int(n)])


class HMCHistoryRule(MappingRule):
    mapping = {
        # specific to macro recorder
        "check <n>":
            R(Function(hmc_checkbox)),
        "check from <n> to <n2>":
            R(Function(hmc_recording_check_range)),
        "exclude <n>":
            R(Function(hmc_recording_exclude)),
        "[make] repeatable":
            R(Function(hmc_recording_repeatable))
    }
    extras = [
        ShortIntegerRef("n", 1, 25),
        ShortIntegerRef("n2", 1, 25),
    ]


def get_rule():
    details = RuleDetails(name="h m c history rule",
                          title=settings.HMC_TITLE_RECORDING)
    return HMCHistoryRule, details
