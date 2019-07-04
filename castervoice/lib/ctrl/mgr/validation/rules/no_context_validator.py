from castervoice.lib.ctrl.mgr.validation.rules.base_validator import BaseRuleValidator

class HasNoContextValidator(BaseRuleValidator):
    def _is_valid(self, rule, params):
        return rule.get_context() is None
    def _invalid_message(self):
        return "must not have a Context"