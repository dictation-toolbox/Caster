from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails


def ccr_global():
    return RuleDetails(ccrtype=CCRType.GLOBAL)


def app_executable(executable):
    return RuleDetails(executable=executable)
