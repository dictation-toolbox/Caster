from castervoice.lib.dfplus.ccrmerging2.validation.base_validator import BaseRuleValidator

class NotNodeRule(BaseRuleValidator):
    def _is_valid(self, rule, params):
        return not hasattr(rule, "master_node")
    def _invalid_message(self):
        return "must not be or inherit NodeRule"