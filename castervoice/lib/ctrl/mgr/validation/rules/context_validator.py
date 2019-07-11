from castervoice.lib.ctrl.mgr.validation.rules.base_validator import BaseRuleValidator


class HasContextValidator(BaseRuleValidator):
    def _is_valid(self, rule):
        return rule.get_context() is not None

    def _invalid_message(self):
        return "must have a Context"
