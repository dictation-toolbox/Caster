from castervoice.lib.ctrl.mgr.validation.rules.base_validator import BaseRuleValidator


class NotNodeRuleValidator(BaseRuleValidator):
    def _is_valid(self, rule):
        return not hasattr(rule, "master_node")

    def _invalid_message(self):
        return "must not be or inherit NodeRule"
