from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.validation.rules.base_validator import BaseRuleValidator


class SelfModifyingRuleValidator(BaseRuleValidator):

    def is_applicable(self, declared_ccrtype):
        return declared_ccrtype == CCRType.SELFMOD

    def _is_valid(self, rule):
        return hasattr(rule, "set_merger")

    def _invalid_message(self):
        return "must be or inherit SelfModifyingRule"
