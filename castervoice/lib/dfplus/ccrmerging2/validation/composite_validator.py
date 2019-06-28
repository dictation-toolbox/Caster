from castervoice.lib.dfplus.ccrmerging2.validation.base_validator import BaseRuleValidator

class CompositeValidator(BaseRuleValidator):
    def __init__(self, validators):
        self._validators = validators
        self._errors = None
    def _is_valid(self, rule, params):
        self._errors = []
        for validator in self._validators:
            error = validator.validate(rule, params)
            if error is not None:
                self._errors.append(error)
        return len(self._errors) == 0
    def _invalid_message(self):
        return ", ".join(self._errors)