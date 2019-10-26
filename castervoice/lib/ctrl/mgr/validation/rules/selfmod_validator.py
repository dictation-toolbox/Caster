from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.validation.rules.base_validator import BaseRuleValidator
from castervoice.lib.merge.selfmod.selfmodrule import BaseSelfModifyingRule


class CCRSelfModifyingRuleValidator(BaseRuleValidator):

    def is_applicable(self, declared_ccrtype):
        return declared_ccrtype == CCRType.SELFMOD

    def _is_valid(self, rule):
        return isinstance(rule, BaseSelfModifyingRule)

    def _invalid_message(self):
        return "must inherit BaseSelfModifyingRule"
