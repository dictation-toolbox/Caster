from castervoice.lib.ctrl.mgr.validation.details.base_validator import BaseDetailsValidator


class CCRDetailsValidator(BaseDetailsValidator):
    """
    Validates any CCR Details
    """

    def validate(self, details):
        invalidations = []
        if details.declared_ccrtype is not None:
            if details.name is not None:
                invalidations.append("ccr types must not have 'name'")
            if details.grammar_name is not None:
                invalidations.append("ccr types must not have 'grammar_name'")

        return None if len(invalidations) == 0 else ", ".join(invalidations)