from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.validation.rules.base_validator import BaseRuleValidator


class NotTreeRuleValidator(BaseRuleValidator):

    def is_applicable(self, declared_ccrtype):
        return declared_ccrtype == CCRType.SELFMOD

    def _is_valid(self, rule):
        return not hasattr(rule, "master_node")

    def _invalid_message(self):
        return "must not be or inherit TreeRule"
