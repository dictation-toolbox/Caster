from castervoice.lib.dfplus.ccrmerging2.validation.base_validator import BaseRuleValidator

class PronunciationAvailableValidator(BaseRuleValidator):
    def _is_valid(self, rule, params):
        existing_pronunciations = params
        return not rule.get_pronunciation() in existing_pronunciations
    def _invalid_message(self):
        return "must have a unique pronunciation"