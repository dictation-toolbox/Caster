class CCRRuleValidationDelegator(object):

    def __init__(self, *validator_delegates):
        self._validator_delegates = validator_delegates

    def validate_rule(self, rule, declared_ccrtype):
        invalidations = []
        for delegate in self._validator_delegates:
            if delegate.is_applicable(declared_ccrtype):
                invalidation = delegate.validate(rule)
                if invalidation is not None:
                    invalidations.append(invalidation)
        return None if len(invalidations) == 0 else ", ".join(invalidation)
