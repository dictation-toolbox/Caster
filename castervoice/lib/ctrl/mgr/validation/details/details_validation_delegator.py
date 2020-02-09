class DetailsValidationDelegator(object):

    def __init__(self, *validator_delegates):
        self._validator_delegates = validator_delegates

    def validate_details(self, details):
        invalidations = []
        for delegate in self._validator_delegates:
            invalidation = delegate.validate(details)
            if invalidation is not None:
                invalidations.append(invalidation)
        return None if len(invalidations) == 0 else ", ".join(invalidations)
