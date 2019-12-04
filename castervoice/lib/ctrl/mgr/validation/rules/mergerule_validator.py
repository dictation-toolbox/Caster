from castervoice.lib.ctrl.mgr.validation.rules.base_validator import BaseRuleValidator
from castervoice.lib.merge.mergerule import MergeRule


class IsMergeRuleValidator(BaseRuleValidator):

    def is_applicable(self, declared_ccrtype):
        return declared_ccrtype is not None

    def _is_valid(self, rule):
        return isinstance(rule, MergeRule)

    def _invalid_message(self):
        return "must be or inherit MergeRule"
