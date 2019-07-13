class BaseRuleValidator(object):

    def is_applicable(self, declared_ccrtype):
        return False

    def _is_valid(self, rule):
        return True

    def _invalid_message(self):
        return "base rule message -- you should not see this"

    def validate(self, rule):
        if not self._is_valid(rule):
            return self._invalid_message()
        else:
            return None
