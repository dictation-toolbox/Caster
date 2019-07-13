from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.validation.rules.base_validator import BaseRuleValidator


class HasNoContextValidator(BaseRuleValidator):

    def is_applicable(self, declared_ccrtype):
        return declared_ccrtype != CCRType.APP

    def _is_valid(self, rule):
        return rule.get_context() is None # TODO -- do we want mergerules to contain their own contexts still? YES

    def _invalid_message(self):
        return "must not have a Context"
