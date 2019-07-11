from castervoice.lib.ctrl.mgr.validation.rules.base_validator import BaseRuleValidator


class CompositeValidator(BaseRuleValidator):

    def __init__(self, validators):
        self._validators = validators
        self._errors = None

    def _is_valid(self, rule):
        self._errors = []
        for validator in self._validators:
            error = validator.validate(rule)
            if error is not None:
                self._errors.append(error)
        return len(self._errors) == 0

    def _invalid_message(self):
        return ", ".join(self._errors)
