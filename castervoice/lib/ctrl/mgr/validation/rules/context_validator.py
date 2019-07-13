from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.validation.rules.base_validator import BaseRuleValidator


class HasContextValidator(BaseRuleValidator):

    def is_applicable(self, declared_ccrtype):
        return declared_ccrtype == CCRType.APP

    def _is_valid(self, rule):
        return rule.get_context() is not None

    def _invalid_message(self):
        return "must have a Context"
