class BaseRuleValidator(object):
    def _is_valid(self, rule, params):
        return True
    def _invalid_message(self):
        return "base rule message -- you should not see this"
    def validate(self, rule, params=None):
        if not self._is_valid(rule, params):
            return self._invalid_message()
        else:
            return None