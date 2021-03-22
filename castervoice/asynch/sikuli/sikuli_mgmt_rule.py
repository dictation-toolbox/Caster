from dragonfly import Function, MappingRule

from castervoice.asynch.sikuli import sikuli_controller
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R
from castervoice.asynch.sikuli import sikuli_gen_rule

_sc = sikuli_controller.get_instance()


class SikuliManagementRule(MappingRule):

    mapping = {
        "launch sick IDE":       R(Function(_sc.launch_IDE)),
        "launch sick server":    R(Function(_sc.bootstrap_start_server_proxy)),
        "terminate sick server": R(Function(_sc.terminate_server_proxy)),
        "refresh sick server":   R(Function(_sc.terminate_server_proxy) + Function(_sc.bootstrap_start_server_proxy)),
    }


def get_rule():
    details = RuleDetails(name="sikuli control rule")
    return SikuliManagementRule, details
