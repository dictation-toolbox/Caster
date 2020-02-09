from castervoice.lib.ctrl.mgr.validation.details.base_validator import BaseDetailsValidator


class NonCCRDetailsValidator(BaseDetailsValidator):
    """
    Validates any non-CCR Details
    """

    def validate(self, details):
        invalidations = []
        if details.declared_ccrtype is None:
            if details.name is None:
                invalidations.append("non-ccr types must have 'name'")
            if details.get_filepath() is None:
                invalidations.append("non-ccr types must not have a filepath")

        return None if len(invalidations) == 0 else ", ".join(invalidations)